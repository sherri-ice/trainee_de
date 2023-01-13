import os
import re


class QueryManager:
    def __init__(self, queries_dir: str = "sql/sql_queries"):
        self._queries_dir = os.path.join(os.getcwd(), queries_dir)
        self._queries_dict = self._load_queries()

    def _load_queries(self):
        query_dict = {}
        for query_type_dict in os.listdir(self._queries_dir): # check if sql
            cur_path = os.path.join(self._queries_dir, query_type_dict)
            for filename in os.listdir(cur_path):
                with open(os.path.join(cur_path, filename), 'r') as file:
                    query_dict[os.path.splitext(filename)[0]] = re.sub(' +', ' ', re.sub('\n', ' ', file.read()))
        print(query_dict)
        return query_dict

    @property
    def queries_dict(self):
        return self._queries_dict

