from task_1.configs.db_config_helper import DBConfigHelper
from sql_connector.sql_connector import SqlConnector
from sql_connector.queries_manager import QueryManager
from object_helper.base_object_helper import BaseObjectHelper

import pandas as pd
from typing import Tuple


class ETL:
    def __init__(self, object_helpers: list[BaseObjectHelper]):
        self.df_data = None
        self.__db_credentials__ = DBConfigHelper().get_credentials()
        self.__db__ = SqlConnector(self.__db_credentials__)
        self.__object_helpers__ = object_helpers
        self.__queries__ = QueryManager().queries_dict
        self._prepare_database()

    def _prepare_database(self):
        self.__db__.create_schema(self.__queries__['create_schema'])
        self.__db__.create_tables(self.__queries__['create_rooms_table'])
        self.__db__.create_tables(self.__queries__['create_students_table'])

    def extract(self) -> list[Tuple[str, pd.DataFrame]]:
        self.df_data = [
            (helper.object_name, helper.load_data_to_df()) for helper in self.__object_helpers__
        ]
        return self.df_data

    def get_list_of_rooms(self):
        query = self.__queries__['list_rooms']
        return pd.read_sql(query, self.__db_credentials__)

    def select_5_lowest_avg_age_rooms(self):
        query = self.__queries__['lowest_avg_age']
        return pd.read_sql(query, self.__db_credentials__)

    def select_5_biggest_age_diff_rooms(self):
        query = self.__queries__['biggest_age_diff']
        return pd.read_sql(query, self.__db_credentials__)

    def select_rooms_with_different_gender(self):
        query = self.__queries__['mixed_gender']
        return pd.read_sql(query, self.__db_credentials__)

    def load(self):
        for table_name, dataframe in self.df_data:
            print(table_name)
            self.__db__.write_df_to_db(
                df=dataframe,
                db_credentials=self.__db_credentials__,
                table_name=table_name
            )
