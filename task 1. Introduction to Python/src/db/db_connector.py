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

    def execute_query(self, query, fetch_policy="all"):
        self.__cursor__.execute(query)
        if fetch_policy == "all":
            return self.__cursor__.fetchall()
        elif fetch_policy == "one":
            return self.__cursor__.fetchone()

    def close_connection(self):
        self.__connection__.close()
