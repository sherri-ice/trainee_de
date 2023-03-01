from datetime import datetime

import pandas as pd
from airflow.decorators import dag, task, task_group
from airflow.models import Variable

from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.pandas_tools import write_pandas

from sql_helper import get_all_table_creation_queries

default_args = {
    'owner': 'sherri-ice'
}


@dag(default_args=default_args, schedule=None, start_date=datetime.utcnow(), catchup=False)
def tasks_flow():
    @task
    def read_csv(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    @task_group
    def prepare_snowflake_database_group(snowflake_cursor: SnowflakeCursor):
        @task
        def create_table(table_sql_query: str) -> None:
            snowflake_cursor.execute(table_sql_query)

        @task
        def create_data_stream(stream_name: str, table_name: str) -> None:
            snowflake_cursor.execute(f'CREATE STREAM IF NOT EXISTS {stream_name} ON TABLE {table_name}')

        project_base_path = Variable.get('PROJECT_BASE_DIR')
        sql_queries = get_all_table_creation_queries(project_base_path)

        create_table.expand(table_sql_query=sql_queries) >> \
        create_data_stream.expand_kwargs(
            [
                {'stream_name': 'raw', 'table_name': 'raw_table'},
                {'stream_name': 'stage', 'table_name': 'stage_table'}
            ]
        )

    @task_group
    def snowflake_load_data_group(data: pd.DataFrame, snowflake_connection: SnowflakeConnection):
        @task
        def load_data_from_pandas_to_raw_table(df: pd.DataFrame,
                                               table_name: str,
                                               snowflake_connection: SnowflakeConnection) -> None:
            write_pandas(snowflake_connection, df, table_name)

        @task
        def load_data_from_raw_to_stage() -> None:
            snowflake_connection.cursor().execute(f'INSERT INTO STAGE_TABLE SELECT * FROM RAW_TABLE')

        @task
        def load_data_from_stage_to_master() -> None:
            snowflake_connection.cursor().execute(f'INSERT INTO MASTER_TABLE SELECT * FROM STAGE_TABLE')

        load_data_from_pandas_to_raw_table(data, 'RAW_TABLE', snowflake_connection) >> \
        load_data_from_raw_to_stage >> load_data_from_stage_to_master

    # Snowflake setup
    snowflake_user = Variable.get('SNOWFLAKE_USER')
    snowflake_password = Variable.get('SNOWFLAKE_PASSWORD')
    snowflake_account = Variable.get('SNOWFLAKE_ACCOUNT')
    snowflake_database = Variable.get('SNOWFLAKE_DATABASE')
    snowflake_schema = Variable.get('SNOWFLAKE_SCHEMA')

    connection = SnowflakeConnection(user=snowflake_user,
                                     password=snowflake_password,
                                     account=snowflake_account,
                                     database=snowflake_database,
                                     schema=snowflake_schema)

    data_path = Variable.get('DATA_PATH')
    data = read_csv(data_path)
    prepare_snowflake_database_group(connection.cursor()) >> snowflake_load_data_group(data, connection)


tasks_flow()
