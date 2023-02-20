from datetime import datetime

import pandas as pd
import pymongo
from airflow.decorators import dag, task, task_group
from airflow.sensors.filesystem import FileSensor
from airflow.models import Variable

default_args = {
    'owner': 'sherri-ice'
}


@dag(default_args=default_args, schedule=None, start_date=datetime.utcnow(), catchup=False)
def tasks_flow():
    @task
    def read_csv(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    @task_group
    def process_data_group(data: pd.DataFrame) -> pd.DataFrame:
        @task
        def drop_empty_rows(data: pd.DataFrame) -> pd.DataFrame:
            data.dropna(how='all', inplace=True)
            return data

        @task
        def replace_null_values(data: pd.DataFrame) -> pd.DataFrame:
            data.fillna(value='-', inplace=True)
            return data

        @task
        def sort_by_created_date(data: pd.DataFrame) -> pd.DataFrame:
            data.sort_values(by='at', inplace=True)
            return data

        @task
        def remove_unnecessary_symbols(data: pd.DataFrame) -> pd.DataFrame:
            data['content'].replace(to_replace=r'[^\w\s.,?!:\'\(\)\-]', value='', regex=True, inplace=True)
            return data

        return remove_unnecessary_symbols(sort_by_created_date(replace_null_values(drop_empty_rows(data))))

    @task
    def load_to_mongo(data: pd.DataFrame):
        mongo_db_conn_str = Variable.get('MONGO_CONN_STR')
        mongo_client = pymongo.MongoClient(mongo_db_conn_str)
        db = mongo_client['reviews']  # creates if not exists
        collection = db['tiktok']
        collection.insert_many(data.to_dict(orient='records'))

    data_path = Variable.get('DATA_PATH')

    file_wait_sensor = FileSensor(task_id='waiting_for_data', filepath=data_path)

    loaded_csv = file_wait_sensor >> read_csv(data_path)
    load_to_mongo(process_data_group(loaded_csv))


tasks_flow()
