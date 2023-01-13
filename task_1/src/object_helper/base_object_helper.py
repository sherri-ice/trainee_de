from abc import ABC, abstractmethod

import pandas as pd


class BaseObjectHelper(ABC):
    def __init__(self, object_name: str, source_file_path: str):
        self._object_name = object_name
        self._source_file_path = source_file_path

    @property
    @abstractmethod
    def object_name(self) -> str:
        ...

    @abstractmethod
    def set_data_source(self, path_to_file: str) -> None:
        ...

    @abstractmethod
    def load_data_to_df(self) -> pd.DataFrame:
        ...
