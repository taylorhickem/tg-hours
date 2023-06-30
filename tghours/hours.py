''' parsing Toggl records into data model
'''
#-----------------------------------------------------
# Import
#-----------------------------------------------------
import json
import pandas as pd
import datetime as dt
from sqlgsheet import database as db
from sqlgsheet.sync import update as sync_update
from tghours.time_series import TimeSeriesTable
from tghours import toggl
#-----------------------------------------------------
# Module variables
#-----------------------------------------------------


#constants
SYNC_FILE = 'dbsync_config.json'
DATE_FORMAT = '%Y-%m-%d'
GS_WKB_NAME = 'hours'
DB_EVENT_TABLE = 'tgevents'
LAST_MODIFIED_FIELD = 'last_modified'
KEY_FIELD = 'timestamp'
WINDOW_YEARS = 1
HRS_IN_WEEK = 168
HRS_IN_DAY = 24
DELIM = '#'
EVENT_FIELDS = ['timestamp', 'date', 'time', 'activity',
                'duration_hrs', 'year', 'month', 'week', 'DOW', 'comment']
MIME_TYPE_CSV = 'text/csv'

#dynamic
events = None


#-----------------------------------------------------
# Setup
#-----------------------------------------------------


def load(source='remote'):
    db_load(source=source)


def db_load(source='remove'):
    if source == 'remote':
        db.DB_SOURCE = 'remote'
    elif source == 'local':
        db.DB_SOURCE = 'local'
        db.SQL_DB_NAME = 'sqlite:///hours.db'
    db.load_sql()


#-----------------------------------------------------
# Procedures
#-----------------------------------------------------


def load_events():
    global events
    events = db.get_table(DB_EVENT_TABLE)
    has_events = not events is None
    if has_events:
        events.set_index('timestamp', inplace=True)
    return has_events


def events_std_format(data, filename='', report_date=None, window_days=None):
    ''' create events from Toggl data table
    '''
    events = []
    try:
        #01 convert the dates and create activity label
        if not report_date:
            report_date = dt.datetime.today().strftime(toggl.TOGGL_DATE_FORMAT)
        if window_days:
            std = toggl.std_events_from_api(report_date, window_days=window_days)
        else:
            std = toggl.std_events_from_api(report_date)

        if len(std) > 0:
            #02 add year, month, week
            events = TimeSeriesTable(std, dtField=KEY_FIELD).ts

    except:
        pass

    return events


def report_update(report_date=None, window_days=None):
    """ updates the database with new events from api and updates google sheet report
    """
    api_rows = events_std_format(None, '', report_date=report_date, window_days=window_days)
    if len(api_rows) > 0:
        api_rows.reset_index(inplace=True)
        db_update(api_rows)
    report_post()


def db_update(api_rows: pd.DataFrame, has_duplicates=True):
    """ updates the database with new events from api
    """
    if db.table_exists(DB_EVENT_TABLE) and has_duplicates:
        unique_rows = remove_duplicates(api_rows)
        if len(unique_rows) > 0:
            db_update(unique_rows, has_duplicates=False)
    else:
        db_rows_insert(api_rows)


def remove_duplicates(api_rows: pd.DataFrame) -> pd.DataFrame:
    """ removes duplicates and returns only unique events from api that are not in the db
    """
    # get the events from the db
    db_events = db_query()

    # add only the new events not already in the database
    not_in_db = pd.concat([db_events, db_events, api_rows])
    not_in_db.drop_duplicates(
        subset=[KEY_FIELD],
        keep=False,
        inplace=True
    )

    return not_in_db


def db_query() -> pd.DataFrame:
    db_events = db.get_table(DB_EVENT_TABLE)
    if db_events is None:
        db_events = pd.DataFrame([])
    else:
        if LAST_MODIFIED_FIELD in db_events:
            del db_events[LAST_MODIFIED_FIELD]
    return db_events


def db_rows_insert(rows: pd.DataFrame):
    with_lm = add_lm_timestamp(rows)
    if db.table_exists(DB_EVENT_TABLE):
        db.rows_insert(with_lm, DB_EVENT_TABLE, con=db.con)
    else:
        db.update_table(with_lm, DB_EVENT_TABLE, append=False)


def add_lm_timestamp(rows: pd.DataFrame) -> pd.DataFrame:
    with_lm = rows.copy()
    if len(with_lm) > 0:
        last_modified = dt.datetime.now()
        with_lm[LAST_MODIFIED_FIELD] = last_modified
    return with_lm


def report_post():
    """ query events from db and publish to the google sheets report
    """
    # 06 format fields for gsheet
    rngcode = 'events'

    # 06.01 date and time to str
    gs_date_format = db.GSHEET_CONFIG[GS_WKB_NAME]['sheets'][rngcode]['date_format']
    time_format = db.GSHEET_CONFIG[GS_WKB_NAME]['sheets'][rngcode]['time_format']

    def event_time_convert(time_value):
        time_str = ''
        if isinstance(time_value, str):
            time_str = time_value[:-3]
        else:
            time_str = time_value.strftime(time_format)
        return time_str

    db_events = db_query()
    db_events['date'] = db_events['date'].apply(lambda x: dt.datetime.strptime(x, DATE_FORMAT))
    db_events['date'] = db_events['date'].apply(lambda x: dt.datetime.strftime(x, gs_date_format))
    db_events['time'] = db_events['time'].apply(lambda x: event_time_convert(x))

    # 06.02 fill empty str for blank comment fields
    db_events['comment'].fillna('', inplace=True)

    # 07 push recent events to gsheet
    min_year = db_events['year'].max() - WINDOW_YEARS + 1
    recent = db_events[db_events['year'] >= min_year].copy()
    db.load_gsheet()
    db.post_to_gsheet(recent[[f for f in EVENT_FIELDS if not f == 'timestamp']],
                      GS_WKB_NAME, rngcode, 'USER_ENTERED')
    db.gs_engine = None


def db_sync():
    sync_update(config_path=SYNC_FILE)
