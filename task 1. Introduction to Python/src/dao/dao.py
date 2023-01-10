# Мб здесь будет класс, которые настраивает бд, взаимодействует с ней.
import json

from db import db_connector as connector


def parse_json_file(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        rows = []
        column_names = []
        for current_dict in data:
            row = []  # maybe ()
            column_names = list(current_dict.keys())
            column_names.remove('id')
            for column_name, value in current_dict.items():
                if column_name == 'id':
                    continue
                row.append(value)
            rows.append(row)
    return column_names, rows


class DAO:
    _db_connector = None

    def __init__(self, db_connector=None):  # поставить по дефолту mysql.connector
        if db_connector is None:
            # todo: get all these params into config file
            # todo: create database if it's not
            print("SQL connector wasn't defined, creating MySQL connector...")
            self._db_connector = connector.DBConnector(
                host="localhost",
                username="user",
                password="password",
                database="hostel"
            )
        else:
            self._db_connector = db_connector

    def _check_table_existence(self, table_name):
        # counts how many tables with given table_name
        sql_query = f"select count(*) from information_schema.tables where table_name = '{table_name}'"
        self._db_connector.execute_query(sql_query)
        result = self._db_connector.fetch_one()
        return result[0] > 0

    def _create_table(self, table_description):
        self._db_connector.execute_query(f"CREATE TABLE {table_description}")

    def _add_rows_to_table(self, table_name, column_names, rows: list):
        # todo: catch exceptions
        sql_query = f"INSERT INTO {table_name} " \
                    f"({', '.join(column_names)}) VALUES ({', '.join(['%s' for i in column_names])})"
        self._db_connector.execute_many_queries(sql_query, rows)
        self._db_connector.commit_changes()

    def _upload_file_to_table(self, json_file_path, table_name):
        column_names, rows = parse_json_file(json_file_path)
        self._add_rows_to_table(table_name, column_names, rows)


class StudentDAO(DAO):

    def __init__(self):
        super().__init__()
        if not self._check_table_existence(table_name="Students"):
            print("Table Students wasn't found, creating it...")
            student_table_description = "Students " \
                                        "(id INT auto_increment PRIMARY KEY, " \
                                        "name VARCHAR(300) not null, " \
                                        "room INT(4) not null, " \
                                        "sex VARCHAR(1) not null, " \
                                        "birthday DATE not null)"
            self._create_table(student_table_description)

    def upload_file(self, json_file_path):
        super()._upload_file_to_table(json_file_path, table_name="Students")

    def get_students(self):
        sql_query = "select * from Students"
        self._db_connector.execute_query(sql_query)
        results = self._db_connector.fetch_all()
        return results


class RoomsDAO(DAO):

    def __init__(self):
        super().__init__()
        if not super()._check_table_existence(table_name="Rooms"):
            print("Table Rooms wasn't found, creating it...")
            room_table_description = "Rooms " \
                                     "(id INT AUTO_INCREMENT primary key, " \
                                     "name VARCHAR(300) not null) "
            self._create_table(room_table_description)

    def upload_file(self, json_file_path):
        super()._upload_file_to_table(json_file_path, table_name="Rooms")

    def get_rooms(self):
        sql_query = "select * from Rooms"
        self._db_connector.execute_query(sql_query)
        results = self._db_connector.fetch_all()
        return results


class StudentRoomMapper:
    ...
