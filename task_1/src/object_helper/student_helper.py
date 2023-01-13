import pandas as pd

from object_helper.base_object_helper import BaseObjectHelper


# todo: non-json files
class StudentHelper(BaseObjectHelper):
    def __init__(self):
        super().__init__(object_name="Students", source_file_path="sample_data/students.json")

    @property
    def object_name(self) -> str:
        return self._object_name

    def set_data_source(self, path_to_file: str) -> None:
        self._source_file_path = path_to_file

    def load_data_to_df(self) -> pd.DataFrame:
        data = pd.read_json(self._source_file_path)
        data['birthday'] = pd.to_datetime(data['birthday'])
        return data
