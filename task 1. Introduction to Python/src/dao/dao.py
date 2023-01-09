# Мб здесь будет класс, которые настраивает бд, взаимодействует с ней.
from db import db_connector as connector
from abc import ABC


class DAO:
    __db_connector = None

    def check_table_existence(self, table_name):
        # counts how many tables with given table_name
        sql_query = f"select count(*) from information_schema.tables where table_name = '{table_name}'"
        result = self.__db_connector.execute_query(sql_query, fetch_policy="one")
        return result[0] > 0

    def create_table(self, table_structure):
        ...

    def upload_to_db_from_file(self, table_name, file_path):
        ...

    def __init__(self, db_connector=None):  # поставить по дефолту mysql.connector
        if db_connector is None:
            # todo: get all these params into config file
            # todo: create database if it's not
            self.__db_connector = connector.DBConnector(
                host="localhost",
                username="user",
                password="password",
                database="hostel"
            )
        else:
            self.__db_connector = db_connector

    def upload_data_to_table(self, table_name):
        ...


class StudentDAO(DAO):

    def upload_data_to_table(self,
                             table_name):  # как заставить аргумент быть постоянным и запретить его менять? мб бахнуть декоарторт)0)0))
        ...

    def get_students(self, condition=None):
        ...


class RoomDAO(DAO):
    def upload_data_to_table(self, table_name):
        ...

    def get_rooms(self, condition=None):
        ...


class StudentRoomMapper():
    ...
