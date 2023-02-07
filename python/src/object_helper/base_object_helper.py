from __future__ import annotations

import os.path
from abc import ABC
from abc import abstractmethod

import pandas as pd

from python.logs.logger import Logger

logger = Logger.__call__().get_logger()


class BaseObjectHelper(ABC):
    def __init__(self, object_name: str, source_file_path: str):
        """
        Base class for further Object Helpers. ObjectHelper stores and loads data from object source.
        Declares abstract methods.

        :param self: Reference the object itself
        :param object_name:str: Store the name of the object
        :param source_file_path:str: Store the path to the source file
        :return: None
        """
        self._object_name = object_name
        if not os.path.exists(source_file_path):
            raise FileNotFoundError(
                f"Source path to {object_name} doesn't exists",
            )
        self._source_file_path = source_file_path

    @property
    @abstractmethod
    def object_name(self) -> str:
        """
        The object_name function returns the name of an object.

        :param self: Access variables that belongs to the class
        :return: The name of the object
        """
        ...

    def set_data_source(self, path_to_file: str):
        """
        The set_data_source function sets the path to the data source file.

        :param self: Access variables that belongs to the class
        :param path_to_file:str: Set the path to the file that will be used as a data source
        :return: None
        """
        self._source_file_path = path_to_file

    @abstractmethod
    def load_data_to_df(self) -> pd.DataFrame:
        """
        The load_data_to_df function extracts the data from a given file and loads it into a pandas DataFrame.

        :param self: Access variables that belongs to the class
        :return: A pandas dataframe
        """
        logger.info(f'Extracting {self._object_name}...')
        ...
