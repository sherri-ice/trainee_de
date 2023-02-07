from __future__ import annotations

from json import JSONDecodeError
from pathlib import Path

import pytest
from sqlalchemy.exc import DBAPIError

from python.sql.configs.db_config_helper import DBConfigHelper
from python.sql.sql_connector.sql_connector import SQLConnector


# todo: Group tests?

@pytest.fixture
def base_path() -> Path:
    """Get the current folder of the selects"""
    return Path(__file__).parent


@pytest.fixture(autouse=True)
def change_test_dir(base_path: Path, monkeypatch):
    monkeypatch.chdir(base_path)


def test_can_parse_db_config():
    DBConfigHelper(config_path='fixtures/test_db_config.json')


def test_not_existing_db_config():
    with pytest.raises(FileNotFoundError):
        DBConfigHelper(config_path='fixtures/not_existing_path.json')


def test_not_json_db_config():
    with pytest.raises(JSONDecodeError):
        DBConfigHelper(config_path='test_db/samples/not_json_db_config.txt')


def test_can_instantiate_db_connection():
    config_helper = DBConfigHelper(
        config_path='test_db/samples/db_config_test.json',
    )
    SQLConnector(config_helper.get_credentials())


def test_wrong_db_credentials():
    config_helper = DBConfigHelper(
        config_path='test_db/samples/db_wrong_config_test.json',
    )
    with pytest.raises(DBAPIError):
        SQLConnector(config_helper.get_credentials())
