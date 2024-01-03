import os
from tghours import hours
import dynamodb
from boto3.dynamodb.conditions import Key, Attr
import datetime as dt

USER_DATA_DIR = '/opt'
API_TOKEN_PATH = USER_DATA_DIR + '/api_token'
db = None

ACTION_TYPE = 'dynamodb_hours_report'
WINDOW_DAYS = None
REPORT_DATE = None
USER_DATA = {}


def lambda_handler(event, context):
    status_code = 500
    message = 'failed'

    if event:
        for param in ['ACTION_TYPE', 'WINDOW_DAYS', 'REPORT_DATE']:
            if param in event:
                globals()[param] = event[param]
        if 'CUTOFF_DATE' in event:
            cutoff_date = event['CUTOFF_DATE']
        else:  # default to past 1 day of records
            cutoff_date = (dt.datetime.now() - dt.timedelta(days=1)).strftime('%Y-%m-%d')

    user_data_load()

    print(f'ACTION_TYPE:{ACTION_TYPE}')

    if ACTION_TYPE == 'dynamodb_hours_report':
        status_code, message = report_update()
    elif ACTION_TYPE == 'delete_recent':
        status_code, message = delete_recent(cutoff_date)
    else:
        status_code = 200
        message = 'no action type defined'

    return {
        'status_code': status_code,
        'message': message
    }


def report_update():
    db_load()
    hours.toggl.API_TOKEN_PATH = API_TOKEN_PATH
    hours.report_update(report_date=REPORT_DATE, window_days=WINDOW_DAYS)

    status_code = 200
    message = 'hours report updated.'

    return status_code, message


def delete_recent(cutoff_date):
    table_name = 'tgevents'

    db_load()
    ddb = hours.db.con
    exp = Attr('date').gte(cutoff_date)
    keys, items = ddb.tables[table_name]._scan(exp)
    ddb.tables[table_name]._items_delete(keys)

    status_code = 200
    message = f'deleted {len(keys)} records from {cutoff_date} to present.'
    return status_code, message


def user_data_load():
    global USER_DATA
    USER_DATA = {
        'gsheet_config': USER_DATA_DIR + '/gsheet_config.json',
        'client_secret': USER_DATA_DIR + '/client_secret.json',
        'dynamodb_config': USER_DATA_DIR + '/dynamodb_config.json'
    }


def db_load():
    hours.db.set_user_data(
        client_secret=USER_DATA['client_secret'],
        gsheet_config=USER_DATA['gsheet_config'],
        db_config=USER_DATA['dynamodb_config']
    )
    hours.db.DB_SOURCE = 'generic'
    hours.db.load(generic_con_class=dynamodb.DynamoDBAPI)
