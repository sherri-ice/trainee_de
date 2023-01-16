from json import JSONDecodeError

import pytest

from pathlib import Path

from sqlalchemy.exc import DBAPIError

from task_1.sql.configs.db_config_helper import DBConfigHelper
from task_1.sql.sql_connector.sql_connector import SqlConnector


# todo: Group tests?

@pytest.fixture
def base_path() -> Path:
    """Get the current folder of the test"""
    return Path(__file__).parent


@pytest.fixture(autouse=True)
def change_test_dir(base_path: Path, monkeypatch):
    monkeypatch.chdir(base_path)


def test_can_parse_db_config():
    config_helper = DBConfigHelper(config_path="samples/db_config_test.json")


def test_not_existing_db_config():
    with pytest.raises(FileNotFoundError):
        config_helper = DBConfigHelper(config_path="samples/not_existing_path.json")


def test_not_json_db_config():
    with pytest.raises(JSONDecodeError):
        config_helper = DBConfigHelper(config_path="samples/not_json_db_config.txt")


def test_can_instantiate_db_connection():
    config_helper = DBConfigHelper(config_path="samples/db_config_test.json")
    db = SqlConnector(config_helper.get_credentials())


def test_wrong_db_credentials():
    config_helper = DBConfigHelper(config_path="samples/db_wrong_config_test.json")
    with pytest.raises(DBAPIError):
        db = SqlConnector(config_helper.get_credentials())
