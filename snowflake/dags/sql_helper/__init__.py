import os
from typing import List
from types import MappingProxyType


class SqlSaveStatements:
    _statements = MappingProxyType({
        ('raw', 'raw_table'): 'CREATE STREAM IF NOT EXISTS raw ON TABLE raw_table;',
        ('stage', 'stage_table'): 'CREATE STREAM IF NOT EXISTS stage ON TABLE stage_table;'
    })

    def _read_sql_file(self, sql_script_path: str) -> str:
        with open(sql_script_path) as file:
            return file.read()

    def get_all_table_creation_queries(self, project_base_path: str) -> List[str]:
        sql_queries = []
        for file in os.listdir(os.path.join(project_base_path, 'dags/sql_helper/create_tables')):
            file_path = os.path.join(
                os.path.join(project_base_path, 'dags/sql_helper/create_tables'), file
            )
            sql_queries.append(self._read_sql_file(file_path))
        return sql_queries

    def get_create_stream_statement(self, stream_name, table_name):
        return self._statements.get((stream_name, table_name))
