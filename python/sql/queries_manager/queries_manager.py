from __future__ import annotations

import os
import re
from collections import defaultdict


class QueryManager:
    def __init__(self, queries_dir: str = 'sql_helper/sql_queries'):
        """
        QueryManager parses and stores SQL queries from queries_dir folder.
        All SQL queries must be written in .sql_helper files.

        :param self: Refer to the object instance from inside the class
        :param queries_dir:str='sql_helper/sql_queries': Tell the class where to look for the queries
        :return: None
        """
        self._queries_dir = os.path.join(os.getcwd(), queries_dir)
        self._queries_dict = self._load_queries()

    def _load_queries(self) -> dict[str, dict[str, str]]:
        """
        The _load_queries function loads the queries from the queries_dir directory.
        It takes in a path to the queries directory and returns a dictionary (type of query)
        of dictionaries (query name to query body).

        :param self: Reference the object itself
        :return: A dictionary of dictionaries of queries
        """
        query_dict: dict[str, dict[str, str]] = defaultdict(lambda: {})
        for query_type_dict in os.listdir(self._queries_dir):  # check if sql_helper
            cur_path = os.path.join(self._queries_dir, query_type_dict)
            for filename in os.listdir(cur_path):
                with open(os.path.join(cur_path, filename)) as file:
                    query_dict[query_type_dict][os.path.splitext(filename)[0]] = \
                        re.sub(' +', ' ', re.sub('\n', ' ', file.read()))
        return query_dict

    @property
    def queries_dict(self) -> dict[str, dict[str, str]]:
        """
        The queries_dict function returns a dictionary of queries. The keys are the query types, and the values are
        dictionary which key is SQL query name and value is the SQL statements to be executed.

        :param self: Represent the instance of the object itself
        :return: A dictionary of dictionaries of queries
        """
        return self._queries_dict
