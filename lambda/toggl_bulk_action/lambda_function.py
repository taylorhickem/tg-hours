import os
from tghours import hours
import datetime as dt

USER_DATA_DIR = '/opt'
API_TOKEN_PATH = USER_DATA_DIR + '/api_token'
db = None
ENV_VARIABLES = [
    'ACTION_TYPE',
    'DATE_START',
    'DATE_END'
]
DATE_START = ''
DATE_END = ''
DATE_FORMAT = hours.toggl.TOGGL_DATE_FORMAT
ACTION_TYPE = 'events_get'
WINDOW_DAYS = 2
REPORT_DATE = None
USER_DATA = {}
response_body = {
    'status_code': 200,
    'message': 'script executed without exception.'
}


def lambda_handler(event, context):
    global response_body

    if event:
        for k in ENV_VARIABLES:
            if k in event:
                globals()[k] = event[k]

    if 'DATE_END' not in event:
        globals()['DATE_END'] = (dt.datetime.now() - dt.timedelta(days=1)).strftime(DATE_FORMAT)

    response_body['request'] = {
        'ACTION_TYPE': ACTION_TYPE,
        'DATE_START': DATE_START,
        'DATE_END': DATE_END
    }

    user_data_load()

    print(f'ACTION_TYPE:{ACTION_TYPE}')

    if ACTION_TYPE == 'events_get':
        status_code, message, data = events_get(DATE_START, DATE_END)
        response_body['data'] = data
    elif ACTION_TYPE == 'events_delete':
        status_code, message = events_delete(DATE_START, DATE_END)
    else:
        status_code = 200
        message = 'no action type defined'

    response_body['status_code'] = status_code
    response_body['message'] = message

    return response_body


def user_data_load():
    global USER_DATA
    USER_DATA = {
        'gsheet_config': USER_DATA_DIR + '/gsheet_config.json',
        'client_secret': USER_DATA_DIR + '/client_secret.json',
        'dynamodb_config': USER_DATA_DIR + '/dynamodb_config.json'
    }


def api_load():
    hours.toggl.API_TOKEN_PATH = API_TOKEN_PATH


def events_get(date_start, date_end):
    status_code = 400
    data = None
    message = f'API ERROR. failed to fetch events start {date_start} to end {date_end} from Toggl API.'

    api_load()

    try:
        hours.toggl.api_login()
        hours.toggl.tz_local = hours.toggl.pytz.timezone(
            hours.toggl.api.auth['timezone']
        )
        search_args = {
            'start_date': date_start,
            'end_date': date_end
        }
        data, status_code = hours.toggl.api.time_entries_search(args=search_args)
        if status_code == 200:
            message = f'success. fetched {len(data)} events start {date_start} to end {date_end} from Toggl API. '

        hours.toggl.api_logout()
    except Exception as e:
        status_code = 400
        message = message + f'\n {str(e)}'

    return status_code, message, data


def events_delete(date_start, date_end):
    status_code = 500
    data = None
    message = f'API ERROR. failed to delete events from start {date_start} to end {date_end} from Toggl API.'

    api_load()

    try:
        hours.toggl.api_login()
        hours.toggl.tz_local = hours.toggl.pytz.timezone(
            hours.toggl.api.auth['timezone']
        )
        message, status_code = hours.toggl.api.delete_time_entries(date_start, date_end)
        hours.toggl.api_logout()
    except Exception as e:
        message = message + f'\n {str(e)}'

    return status_code, message
