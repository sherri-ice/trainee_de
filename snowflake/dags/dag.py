from datetime import datetime

import pandas as pd
from airflow.decorators import dag, task
from airflow.models import Variable

from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.pandas_tools import write_pandas

default_args = {
    'owner': 'sherri-ice'
}


@dag(default_args=default_args, schedule=None, start_date=datetime.utcnow(), catchup=False)
def tasks_flow():
    @task
    def read_csv(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    @task
    def create_data_stream(stream_name: str, table_name: str, snowflake_cursor: SnowflakeCursor) -> None:
        snowflake_cursor.execute(f'CREATE STREAM IF NOT EXISTS {stream_name} ON TABLE {table_name}')

    @task
    def load_data_from_pandas_to_raw_table(df: pd.DataFrame,
                                           table_name: str,
                                           snowflake_connection: SnowflakeConnection) -> None:
        write_pandas(snowflake_connection, df, table_name)

    @task
    def load_data_from_one_table_to_another(source_table_name: str,
                                            target_table_name: str,
                                            snowflake_cursor: SnowflakeCursor):
        snowflake_cursor.execute(f'INSERT INTO {target_table_name} SELECT * FROM {source_table_name}')

    # Snowflake setup
    snowflake_user = Variable.get('SNOWFLAKE_USER')
    snowflake_password = Variable.get('SNOWFLAKE_PASSWORD')
    snowflake_account = Variable.get('SNOWFLAKE_ACCOUNT')
    snowflake_database = Variable.get('SNOWFLAKE_DATABASE')

    connection = SnowflakeConnection(user=snowflake_user,
                                     password=snowflake_password,
                                     account=snowflake_account,
                                     database=snowflake_database)

    data_path = Variable.get('DATA_PATH')
    data = read_csv(data_path)
    create_data_stream.partial(snowflake_cursor=connection).expand_kwargs(
        [
            {'stream_name': 'raw', 'table_name': 'raw_table'},
            {'stream_name': 'stage', 'table_name': 'stage_table'}
        ]
    ) >> \
    load_data_from_pandas_to_raw_table(data, 'RAW_TABLE', connection) >> \
    load_data_from_one_table_to_another('RAW_TABLE', 'STAGE_TABLE', connection.cursor()) >> \
    load_data_from_one_table_to_another('STAGE_TABLE', 'MASTER_TABLE', connection.cursor())


tasks_flow()
