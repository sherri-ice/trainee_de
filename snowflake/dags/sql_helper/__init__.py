import os
from typing import List


def _read_sql_file(sql_script_path: str) -> str:
    with open(sql_script_path) as file:
        return file.read()


def get_all_table_creation_queries(project_base_path: str) -> List[str]:
    sql_queries = []
    for file in os.listdir(os.path.join(project_base_path, 'dags/sql_helper/create_tables')):
        file_path = os.path.join(
            os.path.join(project_base_path, 'dags/sql_helper/create_tables'), file
        )
        sql_queries.append(_read_sql_file(file_path))
    return sql_queries


if __name__ == '__main__':
    l = get_all_table_creation_queries()
    print(l)
