import os
import json
import pandas as pd
from sqlgsheet import database as db
import boto3
from tghours import hours

USER_DATA_DIR = '/opt'
API_TOKEN_PATH = USER_DATA_DIR + '/api_token'
user_data = {
    'gsheet_config': USER_DATA_DIR + '/gsheet_config.json',
    'client_secret': USER_DATA_DIR + '/client_secret.json',
    'mysql_credentials': USER_DATA_DIR + '/mysql_credentials.json'
}

s3_client = None


def lambda_handler(event, context):
    report_date = None
    window_days = None
    status_code = 500
    message = 'failed'
    
    hours.db.set_user_data(
        client_secret=user_data['client_secret'],
        gsheet_config=user_data['gsheet_config'],
        mysql_credentials=user_data['mysql_credentials']
    )
    hours.toggl.API_TOKEN_PATH = API_TOKEN_PATH
    hours.db.DB_SOURCE = 'remote'
    
    hours.db_load()
    hours.report_update(report_date=report_date, window_days=window_days)

    status_code = 200
    message = 'hours report updated.'

    return {
        'status_code': status_code,
        'message': message
    }