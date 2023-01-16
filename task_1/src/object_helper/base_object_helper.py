from __future__ import annotations

import os.path
from abc import ABC
from abc import abstractmethod

from task_1.logs.logger import Logger

logger = Logger.__call__().get_logger()


class BaseObjectHelper(ABC):
    def __init__(self, object_name: str, source_file_path: str):
        self._object_name = object_name
        if not os.path.exists(source_file_path):
            raise FileNotFoundError(
                f"Source path to {object_name} doesn't exists",
            )
        self._source_file_path = source_file_path

    @property
    @abstractmethod
    def object_name(self) -> str:
        ...

    def set_data_source(self, path_to_file: str) -> None:
        self._source_file_path = path_to_file

    def load_data_to_df(self):
        logger.info(f'Extracting {self._object_name}...')
