from __future__ import annotations

import os

import pandas as pd
from object_helper.base_object_helper import BaseObjectHelper

from python.logs.logger import Logger
from python.sql.configs.db_config_helper import DBConfigHelper
from python.sql.queries_manager.queries_manager import QueryManager
from python.sql.sql_connector.sql_connector import SQLConnector

logger = Logger.__call__().get_logger()


class ETL:
    def __init__(self, db_config_path: str, sql_queries_dir: str, object_helpers: list[BaseObjectHelper]):
        """
        Initializes database connection, QueryManager, creates schema and tables for execution.

        :param self: Refer to the object itself
        :param db_config_path:str: Pass the path to the database configuration file
        :param sql_queries_dir:str: Tell the QueryManager where to look for the queries
        :param object_helpers:list[BaseObjectHelper]: Store the list of object helpers
        :return: None
        """
        self.__db_credentials__ = DBConfigHelper(
            config_path=db_config_path,
        ).get_credentials()
        self.__db__ = SQLConnector(self.__db_credentials__)
        self.__object_helpers__ = object_helpers
        self.__queries__ = QueryManager(
            queries_dir=sql_queries_dir,
        ).queries_dict
        self._prepare_database()

    def _prepare_database(self):
        """
        The _prepare_database function creates the database schema and tables
        necessary for the program to run. It is called by __init__, which is executed
        when a new instance of this class is created.

        :param self: Access the attributes and methods of the class in python
        :return: None
        """
        self.__db__.create_schema(
            self.__queries__['creation']['create_schema'],
        )
        self.__db__.create_tables(
            self.__queries__['creation']['create_rooms_table'],
        )
        self.__db__.create_tables(
            self.__queries__['creation']['create_students_table'],
        )

    def extract(self) -> list[tuple[str, pd.DataFrame]]:
        """
        The extract function returns a list of tuples, where each tuple contains the name of an object and its
        corresponding dataframe.


        :param self: Access the attributes and methods of the class in python
        :return: A list of tuples
        """
        self.df_data = [
            (helper.object_name, helper.load_data_to_df()) for helper in self.__object_helpers__
        ]
        return self.df_data

    def do_select_query(self, query_name: str) -> pd.DataFrame:
        """
        The do_select_query function is used to execute a select query from the queries.sql_helper file.
        The function takes in a string as an argument, which is the name of the query you want to run.
        It returns a pandas dataframe containing all of your results.

        :param self: Access the class attributes
        :param query_name:str: Specify which query to run
        :return: A pandas dataframe of the query
        """
        return pd.read_sql(self.__queries__['selects'][query_name], self.__db_credentials__)

    def export_results(self, query_name: str, output_format: str = 'json'):
        """
        The export_results function exports the results of a query to a specified format.
        The function takes two arguments:
            - query_name: The name of the SQL query to be executed. This is used as an identifier for the output file,
            and should correspond with one of the queries defined in `sql_helper/sql_queries/selects`
            - output_format: The format in which you want your results exported. Currently supported formats are 'json'
            and 'xml'. Defaults to json if not specified.

        :param self: Access the class attributes and methods
        :param query_name:str: Specify the name of the query that is being run
        :param output_format:str='json': Specify the format of the output file
        :return: None
        """
        logger.info(f'Starting query: {query_name}')
        try:
            df = self.do_select_query(query_name=query_name)
        except Exception as exp:
            logger.exception(exp)
            raise exp
        logger.info(f'Query {query_name} successfully ended')
        output_dir = os.path.join(os.getcwd(), f'output/{output_format}')
        output_path = os.path.join(output_dir, f'{query_name}.{output_format}')
        logger.info(f'Saving results to {output_path}')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if output_format == 'json':
            df.to_json(output_path)
        elif output_format == 'xml':
            df.to_xml(output_path)

    def load(self):
        """
        The load function writes the dataframe to a table in the database.
        It uses inner self.df_data:
            - A list of tuples, where each tuple contains a table name and a dataframe.

        :param self: Access the class attributes
        :return: None
        """
        for table_name, dataframe in self.df_data:
            logger.info(f'Writing {table_name} to database...')
            self.__db__.write_df_to_db(
                df=dataframe,
                db_credentials=self.__db_credentials__,
                table_name=table_name,
            )

    def do_all_selects_and_export_results(self, output_format: str = 'json'):
        """
        The do_all_selects_and_export_results function loops through all the select functions in the
        sql_helper/sql_queries/selects directory, and executes them and exports their results to a JSON or xml file depending
        on what output_format is set to.

        :param self: Access the class attributes
        :param output_format:str='json': Specify the format of the output
        :return: None
        """
        for func in self.__queries__['selects'].keys():
            self.export_results(func, output_format=output_format)
