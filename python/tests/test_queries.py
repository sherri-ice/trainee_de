from __future__ import annotations

from pathlib import Path

import pytest

from python.sql.queries_manager.queries_manager import QueryManager


@pytest.fixture
def base_path() -> Path:
    """Get the current folder of the selects"""
    return Path(__file__).parent


@pytest.fixture(autouse=True)
def change_test_dir(base_path: Path, monkeypatch):
    monkeypatch.chdir(base_path)


def test_check_query_manager():
    query_manager = QueryManager(queries_dir='fixtures/queries')
    assert len(query_manager.queries_dict) == 1


def test_query_manager_with_not_existing_dir():
    with pytest.raises(FileNotFoundError):
        QueryManager(queries_dir='fixtures/not_existing')
