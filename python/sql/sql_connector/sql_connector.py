from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import DBAPIError

from python.logs.logger import Logger

logger = Logger.__call__().get_logger()


class SQLConnector:

    def __init__(self, db_credentials: str):
        """
        SQLConnector helps to connect to the database's API and do some executes.

        :param self: Reference the object itself
        :param db_credentials:str: Pass the database connection string to the class
        :return: None
        """
        logger.info('Creating connection to database...')
        self.__engine__ = create_engine(db_credentials)
        try:
            self.__engine_connect__ = self.__engine__.connect()
        except DBAPIError as exp:
            logger.exception(exp)
            raise exp
        logger.info('Connection created successful')

    def create_schema(self, schema_query) -> CursorResult:
        """
        The create_schema function creates a schema in the database.
        It takes one argument, which is a string containing the query to create the schema.

        :param self: Access the class attributes
        :param schema_query: Create a new schema in the database
        :return: A CursorResult object
        """
        return self.__engine_connect__.execute(schema_query)

    def create_tables(self, tables_query) -> CursorResult:
        """
        The create_tables function creates the tables in the database.
        It takes a list of queries as an argument, and executes them using the engine connection.

        :param self: Access the class attributes and methods
        :param tables_query: Create the tables
        :return: A CursorResult object
        """
        return self.__engine_connect__.execute(tables_query, multi=True)

    def execute_query(self, query: str):
        """
        The execute_query function is a helper function that executes the query passed to it.
        It returns the result of the query.

        :param self: Access the class attributes and methods
        :param query:str: Pass a sql_helper query to the execute_query function
        :return: The result of the query
        """
        return self.__engine_connect__.execute(query)

    @staticmethod
    def write_df_to_db(df: pd.DataFrame, db_credentials: str, table_name: str, schema: str = 'hostel'):
        """
        The write_df_to_db function writes a dataframe to a database.

        :param df:pd.DataFrame: Specify the dataframe that is to be written to the database
        :param db_credentials:str: Pass the database credentials
        :param table_name:str: Specify the name of the table that will be created/edited in the database
        :param schema:str='hostel': Specify the schema in which the table will be written
        :return: None
        """
        df.to_sql(
            name=table_name,
            con=db_credentials,
            schema=schema,
            if_exists='replace',
            index=False,
        )
