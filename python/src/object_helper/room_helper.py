from __future__ import annotations

import pandas as pd
from object_helper.base_object_helper import BaseObjectHelper


class RoomHelper(BaseObjectHelper):

    def __init__(self, source_file_path='sample_data/rooms.json'):
        """
         Object helper for Room.

        :param self: Refer to the object instance
        :param source_file_path='sample_data/rooms.json': Specify the path to the file that contains the data
        :return: None
        """
        super().__init__(object_name='Rooms', source_file_path=source_file_path)

    @property
    def object_name(self) -> str:
        """
        The object_name function returns the name of an object.

        :param self: Access variables that belongs to the class
        :return: The name of the object
        """
        return self._object_name

    def load_data_to_df(self) -> pd.DataFrame:
        """
        The load_data_to_df function extracts the data from a given file and loads it into a pandas DataFrame.

        :param self: Access variables that belongs to the class
        :return: A pandas dataframe
        """
        super().load_data_to_df()
        return pd.read_json(self._source_file_path)
