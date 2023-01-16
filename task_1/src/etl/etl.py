import os

from task_1.sql.configs.db_config_helper import DBConfigHelper
from task_1.sql.sql_connector.sql_connector import SqlConnector
from task_1.sql.queries_manager.queries_manager import QueryManager
from object_helper.base_object_helper import BaseObjectHelper
from task_1.logs.logger import Logger

import pandas as pd
from typing import Tuple

logger = Logger.__call__().get_logger()


class ETL:
    def __init__(self, db_config_path, sql_queries_dir, object_helpers: list[BaseObjectHelper]):
        self.df_data = None
        self.__db_credentials__ = DBConfigHelper(config_path=db_config_path).get_credentials()
        self.__db__ = SqlConnector(self.__db_credentials__)
        self.__object_helpers__ = object_helpers
        self.__queries__ = QueryManager(queries_dir=sql_queries_dir).queries_dict
        self._prepare_database()

    def _prepare_database(self):
        self.__db__.create_schema(self.__queries__['creation']['create_schema'])
        self.__db__.create_tables(self.__queries__['creation']['create_rooms_table'])
        self.__db__.create_tables(self.__queries__['creation']['create_students_table'])

    def extract(self) -> list[Tuple[str, pd.DataFrame]]:
        self.df_data = [
            (helper.object_name, helper.load_data_to_df()) for helper in self.__object_helpers__
        ]
        return self.df_data

    def do_select_query(self, query_name: str):
        return pd.read_sql(self.__queries__['selects'][query_name], self.__db_credentials__)

    def export_results(self, query_name: str, output_format: str = 'json'):
        logger.info(f"Starting query: {query_name}")
        try:
            df = self.do_select_query(query_name=query_name)
        except Exception as exp:
            logger.exception(exp)
            raise exp
        logger.info(f"Query {query_name} successfully ended")
        output_dir = os.path.join(os.getcwd(), f'output/{output_format}')
        output_path = os.path.join(output_dir, f'{query_name}.{output_format}')
        logger.info(f"Saving results to {output_path}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if output_format == 'json':
            df.to_json(output_path)
        elif output_format == 'xml':
            df.to_xml(output_path)

    def load(self):
        for table_name, dataframe in self.df_data:
            logger.info(f"Writing {table_name} to database...")
            self.__db__.write_df_to_db(
                df=dataframe,
                db_credentials=self.__db_credentials__,
                table_name=table_name
            )

    def do_all_selects_and_export_results(self, output_format='json'):
        for func in self.__queries__['selects'].keys():
            self.export_results(func, output_format=output_format)
