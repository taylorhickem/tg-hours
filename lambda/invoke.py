from tghours import hours
import dynamodb


USER_DATA_DIR = '/opt'
API_TOKEN_PATH = USER_DATA_DIR + '/api_token'


USER_DATA = {}
s3_client = None


def lambda_handler(event, context):
    report_date = None
    window_days = None
    status_code = 500
    message = 'failed'

    user_data_load()
    db_load()
    hours.toggl.API_TOKEN_PATH = API_TOKEN_PATH
    hours.report_update(report_date=report_date, window_days=window_days)

    status_code = 200
    message = 'hours report updated.'

    return {
        'status_code': status_code,
        'message': message
    }


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
