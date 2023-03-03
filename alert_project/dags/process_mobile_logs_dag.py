import os
from datetime import datetime, timedelta
from typing import List

import pandas as pd
from airflow.decorators import dag, task, task_group
from airflow.models import Variable

from config_storage import EmailStorage, SchemaStorage

default_args = {
    'owner': 'sherri-ice',
    'email': EmailStorage(os.getenv('EMAIL_CONFIG_PATH')).email_list,
    'email_on_failure': 'True',
}


@dag(dag_id='process_mobile_logs', default_args=default_args, schedule=timedelta(minutes=10),
     start_date=datetime.utcnow(), catchup=False)
def process_mobile_logs():
    @task_group
    def prepare_logs():
        @task
        def read_logs_from_csv(log_csv_path: str) -> pd.DataFrame:
            return pd.read_csv(log_csv_path)

        @task
        def rename_df_columns(df: pd.DataFrame, new_column_names: List[str]) -> pd.DataFrame:
            df.columns = new_column_names
            df['date'] = pd.to_datetime(df['date'])
            return df

        data_path = Variable.get('DATA_PATH')
        schema_config_path = Variable.get('SCHEMA_CONFIG_PATH')
        new_column_names = SchemaStorage(schema_config_path).schema_config

        data = read_logs_from_csv(data_path)
        rename_df_columns(data, new_column_names)

    prepare_logs()


process_mobile_logs()
