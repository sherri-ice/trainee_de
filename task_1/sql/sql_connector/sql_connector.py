from task_1.logs.logger import Logger

from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError

import pandas as pd

logger = Logger.__call__().get_logger()


class SqlConnector:

    def create_schema(self, schema_query):
        return self.__engine_connect__.execute(schema_query)

    def create_tables(self, tables_query):
        return self.__engine_connect__.execute(tables_query, multi=True)

    def __init__(self, db_credentials: str):
        logger.info("Creating connection to database...")
        self.__engine__ = create_engine(db_credentials)
        try:
            self.__engine_connect__ = self.__engine__.connect()
        except DBAPIError as exp:
            logger.exception(exp)
            raise exp
        logger.info("Connection created successful")

    def execute_query(self, query: str):
        return self.__engine_connect__.execute(query)

    @staticmethod
    def write_df_to_db(df: pd.DataFrame, db_credentials: str, table_name: str, schema: str = "hostel") -> None:
        df.to_sql(
            name=table_name,
            con=db_credentials,
            schema=schema,
            if_exists='replace',
            index=False
        )
