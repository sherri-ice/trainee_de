# коннектор и execute'ы сюда
import mysql.connector


class DBConnector:
    def __init__(self, host, username, password, database):
        # try и логи на проверку коннекшена
        self.__connection__ = mysql.connector.connect(
            host=host,
            username=username,
            password=password,
            database=database
        )
        self.__cursor__ = self.__connection__.cursor()

    def execute_query(self, query):
        self.__cursor__.execute(query)

    def execute_many_queries(self, query, values):
        self.__cursor__.executemany(query, values)

    def fetch_all(self):
        return self.__cursor__.fetchall()

    def fetch_one(self):
        return self.__cursor__.fetchone()

    def commit_changes(self):
        self.__connection__.commit()

    def close_connection(self):
        self.__connection__.close()

