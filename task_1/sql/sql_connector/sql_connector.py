from sqlalchemy import create_engine

import pandas as pd


class SqlConnector:

    def create_schema(self, schema_query):
        return self.__engine_connect__.execute(schema_query)

    def create_tables(self, tables_query):
        return self.__engine_connect__.execute(tables_query, multi=True)

    def __init__(self, db_credentials: str):
        # todo: try и логи на проверку коннекшена
        self.__engine__ = create_engine(db_credentials)
        self.__engine_connect__ = self.__engine__.connect()

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

    def get_df_from_db(self):
        ...
