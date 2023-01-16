from __future__ import annotations

import pandas as pd
from object_helper.base_object_helper import BaseObjectHelper


# todo: non-json files
class StudentHelper(BaseObjectHelper):
    def __init__(self, source_file_path='sample_data/students.json'):
        """
        Object helper for Student.

        :param self: Refer to the object itself
        :param source_file_path='sample_data/students.json': Specify the path of the json file
        :return: A new instance of the student class
        """
        super().__init__(object_name='Students', source_file_path=source_file_path)

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
        Converts date to pd.Datetime.

        :param self: Access variables that belongs to the class
        :return: A pandas dataframe
        """
        super().load_data_to_df()
        data = pd.read_json(self._source_file_path)
        data['birthday'] = pd.to_datetime(data['birthday'])
        return data
