import json
import os
from _decimal import Decimal

import boto3
import botocore.exceptions
import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

aws_endpoint_url = f"http://{os.getenv('LOCALSTACK_HOSTNAME')}:4566"
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
aws_region_name = os.getenv('AWS_REGION_NAME')

s3_resource = boto3.resource('s3',
                             endpoint_url=aws_endpoint_url,
                             aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key,
                             region_name=aws_region_name)

dynamodb_resource = boto3.resource('dynamodb',
                                   endpoint_url=aws_endpoint_url,
                                   aws_access_key_id=aws_access_key,
                                   aws_secret_access_key=aws_secret_key,
                                   region_name=aws_region_name)


def _check_if_file_loaded_to_s3(bucket_name: str, filename_key: str) -> bool:
    try:
        s3_resource.Object(bucket_name, filename_key).load()
    except botocore.exceptions.ClientError as err:
        return False
    return True


def _read_csv_from_s3_bucket(bucket_name: str, filename_key: str) -> pd.DataFrame:
    s3_bucket_obj = s3_resource.Object(bucket_name=bucket_name, key=filename_key)
    return pd.read_csv(s3_bucket_obj.get()['Body'], parse_dates=['departure']).fillna(0)


def _load_metrics_to_dynamodb(df: pd.DataFrame) -> None:
    helsinki_city_bikes_daily_metrics_table = dynamodb_resource.Table('helsinki_city_bikes_daily_metrics')
    for group_name, group in df.groupby(pd.Grouper(key='departure', freq='D')):
        if not group.empty:
            with helsinki_city_bikes_daily_metrics_table.batch_writer(overwrite_by_pkeys=['date']) as batch_writer:
                batch_writer.put_item(
                    Item={'date': f'{group_name:%Y-%m-%d}',
                          'avg_distance_m': Decimal(str(df['distance (m)'].mean())),
                          'avg_duration_sec': Decimal(str(df['duration (sec.)'].mean())),
                          'avg_speed_km_h': Decimal(str(df['avg_speed (km/h)'].mean())),
                          'avg_air_temperature_c': Decimal(str(df['Air temperature (degC)'].mean()))})


def lambda_handler(event, context):
    for key in ['metrics/result.csv', 'data/dataset.csv']:
        if not _check_if_file_loaded_to_s3(bucket_name='helsinki-city-bikes', filename_key=key):
            logger.info(f"{key} was not loaded to bucket, waiting for lambda revoke...")
            return

    event_body = event['Records'][0]['Sns']['Message']
    helsinki_city_bikes_key = json.loads(event_body)['Records'][0]['s3']['object']['key']

    df = _read_csv_from_s3_bucket(bucket_name='helsinki-city-bikes', filename_key=helsinki_city_bikes_key)
    _load_metrics_to_dynamodb(df)
