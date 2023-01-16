from __future__ import annotations

import os.path
import shutil
from pathlib import Path

import pandas as pd
import pytest
import sqlalchemy

from task_1.sql.configs.db_config_helper import DBConfigHelper
from task_1.src.etl.etl import ETL
from task_1.src.object_helper.room_helper import RoomHelper
from task_1.src.object_helper.student_helper import StudentHelper


@pytest.fixture
def base_path() -> Path:
    """Get the current folder of the selects"""
    return Path(__file__).parent


@pytest.fixture(autouse=True)
def change_test_dir(base_path: Path, monkeypatch):
    monkeypatch.chdir(base_path)


@pytest.fixture
def db_connection():
    credentials = DBConfigHelper(
        'fixtures/test_db_config.json',
    ).get_credentials()
    engine = sqlalchemy.create_engine(credentials)
    connection = engine.connect()
    return connection


helpers_dict = {
    'Rooms': RoomHelper('fixtures/test_rooms.json'),
    'Students': StudentHelper('fixtures/test_students.json'),
}


@pytest.fixture
def etl_obj(mocker, db_connection):
    def create_schema(self):
        db_connection.execute('create schema if not exists hostel;')

    def prepare_database(self):
        create_schema(self)
        db_connection.execute(
            'create table if not exists hostel.Rooms '
            '(id int auto_increment primary key not null , '
            'name varchar(50) not null);',
        )
        db_connection.execute(
            'create table if not exists hostel.Students '
            '(birthday date not null, '
            'id int auto_increment not null primary key, '
            'name varchar(300) not null, '
            'room int not null, '
            'sex char(1) not null, '
            'foreign key (room) references hostel.Rooms(id) on delete cascade);',
        )

    mocker.patch('task_1.src.etl.etl.ETL._prepare_database', prepare_database)

    rooms_helper = RoomHelper('fixtures/test_rooms.json')
    students_helper = StudentHelper('fixtures/test_students.json')
    return ETL(
        db_config_path='fixtures/test_db_config.json',
        sql_queries_dir='fixtures/queries',
        object_helpers=[rooms_helper, students_helper],
    )


def test_can_create_schema_and_tables(etl_obj, db_connection):
    etl_obj._prepare_database()
    cursor = db_connection.execute(
        "select schema_name from information_schema.SCHEMATA where SCHEMA_NAME='hostel';",
    )
    result = cursor.fetchone()
    assert len(result) == 1
    assert result[0] == 'hostel'

    cursor = db_connection.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_name = 'Students';",
    )
    result = cursor.fetchone()
    assert len(result) == 1

    cursor = db_connection.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_name = 'Rooms';",
    )
    result = cursor.fetchone()
    assert len(result) == 1


def test_etl_extract(etl_obj, db_connection):
    data = etl_obj.extract()
    for data_tuple in data:
        assert data_tuple[0] in helpers_dict
        assert isinstance(data_tuple[1], pd.DataFrame)
        pd.testing.assert_frame_equal(
            data_tuple[1],
            helpers_dict[data_tuple[0]].load_data_to_df(),
        )


def test_etl_load(etl_obj, db_connection):
    etl_obj._prepare_database()
    etl_obj.extract()
    etl_obj.load()
    results = db_connection.execute('SELECT 1 FROM hostel.Rooms').fetchall()
    assert len(results) == len(helpers_dict['Rooms'].load_data_to_df())
    results = db_connection.execute('SELECT 1 FROM hostel.Students').fetchall()
    assert len(results) == len(helpers_dict['Students'].load_data_to_df())


def test_etl_export_results(etl_obj, db_connection):
    etl_obj.do_all_selects_and_export_results()
    queries = etl_obj.__queries__
    for query_name in queries['selects'].keys():
        assert os.path.exists(
            os.path.join(
                os.getcwd(), f'output/json/{query_name}.json',
            ),
        )
    shutil.rmtree(os.path.join(os.getcwd(), 'output/'))
