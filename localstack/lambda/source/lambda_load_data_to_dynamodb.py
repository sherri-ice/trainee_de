import json
import logging
import os
from _decimal import Decimal

import boto3
import botocore.exceptions
import pandas as pd

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
    session = boto3.session.Session()
    s3_client = session.client('s3',
                               endpoint_url=aws_endpoint_url,
                               aws_access_key_id=aws_access_key,
                               aws_secret_access_key=aws_secret_key,
                               region_name=aws_region_name)
    logger.info(f"Start pinging {filename_key} for head_object...")
    try:
        s3_client.head_object(Bucket=bucket_name, Key=filename_key)
    except botocore.exceptions.ClientError:
        logger.info(f"{filename_key} was not loaded to bucket, waiting for lambda revoke...")
        return False
    except:
        logger.info(f"Connection reset")
        return False
    logger.info(f"{filename_key} found")
    return True


def _read_csv_from_s3_bucket(bucket_name: str, filename_key: str) -> pd.DataFrame:
    s3_bucket_obj = s3_resource.Object(bucket_name=bucket_name, key=filename_key)
    return pd.read_csv(s3_bucket_obj.get()['Body'], parse_dates=['departure']).fillna(0)


def _load_common_metrics_by_period(df: pd.DataFrame, period: str, table: dynamodb_resource.Table) -> None:
    for group_name, group in df.groupby(pd.Grouper(key='departure', freq=period)):
        if not group.empty:
            with table.batch_writer(overwrite_by_pkeys=['date']) as batch_writer:
                batch_writer.put_item(
                    Item={'date': f'{group_name:%Y-%m-%d}',
                          'avg_distance_m': Decimal(str(df['distance (m)'].mean())),
                          'avg_duration_sec': Decimal(str(df['duration (sec.)'].mean())),
                          'avg_speed_km_h': Decimal(str(df['avg_speed (km/h)'].mean())),
                          'avg_air_temperature_c': Decimal(str(df['Air temperature (degC)'].mean()))})


def _load_raw_data(df: pd.DataFrame, table: dynamodb_resource.Table) -> None:
    with table.batch_writer(overwrite_by_pkeys=['departure_id', 'return_id']) as batch_writer:
        for _, row in df.iterrows():
            batch_writer.put_item(Item={'departure': row['departure'],
                                        'return': row['return'],
                                        'departure_id': int(row['departure_id']),
                                        'departure_name': row['departure_name'],
                                        'return_id': int(row['return_id']),
                                        'return_name': row['return_name'],
                                        'distance (m)': int(row['distance (m)']),
                                        'duration (sec.)': int(row['duration (sec.)']),
                                        'avg_speed (km/h)': Decimal(str(row['avg_speed (km/h)'])),
                                        'departure_latitude': Decimal(str(row['departure_latitude'])),
                                        'departure_longitude': Decimal(str(row['departure_longitude'])),
                                        'return_latitude': Decimal(str(row['return_latitude'])),
                                        'return_longitude': Decimal(str(row['return_longitude'])),
                                        'Air temperature (degC)': Decimal(str(row['Air temperature (degC)']))})


def _load_station_metrics(df: pd.DataFrame, table: dynamodb_resource.Table) -> None:
    with table.batch_writer(overwrite_by_pkeys=['station_name']) as batch_writer:
        for _, row in df.iterrows():
            batch_writer.put_item(Item={'station_name': row['station_name'],
                                        'departure_count': int(row['departure_count']),
                                        'return_count': int(row['return_count'])})


def lambda_handler(event, context):
    for key in ['metrics/result.csv', 'data/dataset.csv']:
        if not _check_if_file_loaded_to_s3(bucket_name='helsinki-city-bikes', filename_key=key):
            return

    event_body = event['Records'][0]['Sns']['Message']
    helsinki_city_bikes_key = json.loads(event_body)['Records'][0]['s3']['object']['key']

    logger.info(f"Read {helsinki_city_bikes_key}...")
    df = _read_csv_from_s3_bucket(bucket_name='helsinki-city-bikes', filename_key=helsinki_city_bikes_key)
    logger.info(f"Uploaded {helsinki_city_bikes_key}...")

    # Load daily metrics
    helsinki_city_bikes_daily_metrics_table = dynamodb_resource.Table('helsinki_city_bikes_daily_metrics')
    _load_common_metrics_by_period(df, 'D', helsinki_city_bikes_daily_metrics_table)

    # Load monthly metrics
    helsinki_city_bikes_monthly_metrics_table = dynamodb_resource.Table('helsinki_city_bikes_monthly_metrics')
    _load_common_metrics_by_period(df, 'M', helsinki_city_bikes_monthly_metrics_table)

    # Load raw data
    helsinki_city_bikes_raw_table = dynamodb_resource.Table('helsinki_city_bikes_raw')
    _load_raw_data(df, helsinki_city_bikes_raw_table)

    # Load station metrics
    helsinki_city_bikes_station_metrics_table = dynamodb_resource.Table('helsinki_city_bikes_station_metrics')
    _load_station_metrics(df, helsinki_city_bikes_station_metrics_table)
