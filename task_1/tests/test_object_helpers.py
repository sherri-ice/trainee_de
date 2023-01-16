from pathlib import Path

import pandas as pd
import pytest

from task_1.src.object_helper.room_helper import RoomHelper
from task_1.src.object_helper.student_helper import StudentHelper


@pytest.fixture
def base_path() -> Path:
    """Get the current folder of the selects"""
    return Path(__file__).parent


@pytest.fixture(autouse=True)
def change_test_dir(base_path: Path, monkeypatch):
    monkeypatch.chdir(base_path)


def test_object_helper():
    StudentHelper(source_file_path="fixtures/test_students.json")
    RoomHelper(source_file_path="fixtures/test_rooms.json")


def test_object_helper_with_not_existing_source():
    with pytest.raises(FileNotFoundError):
        StudentHelper(source_file_path="fixtures/doesnt_exist.json")


def test_load_students():
    student_helper = StudentHelper(source_file_path="fixtures/test_students.json")
    actual = student_helper.load_data_to_df()
    expected = pd.read_json("fixtures/test_students.json")
    expected['birthday'] = pd.to_datetime(expected['birthday'])
    assert isinstance(actual, pd.DataFrame)
    assert len(actual) == len(expected)
    pd.testing.assert_frame_equal(actual, expected)


def test_load_rooms():
    student_helper = RoomHelper(source_file_path="fixtures/test_rooms.json")
    actual = student_helper.load_data_to_df()
    expected = pd.read_json("fixtures/test_rooms.json")
    assert isinstance(actual, pd.DataFrame)
    assert len(actual) == len(expected)
    pd.testing.assert_frame_equal(actual, expected)
