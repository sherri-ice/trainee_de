import pandas as pd

from object_helper.base_object_helper import BaseObjectHelper


# todo: non-json files
class StudentHelper(BaseObjectHelper):
    def __init__(self, source_file_path="sample_data/students.json"):
        super().__init__(object_name="Students", source_file_path=source_file_path)

    @property
    def object_name(self) -> str:
        return self._object_name

    def load_data_to_df(self) -> pd.DataFrame:
        super().load_data_to_df()
        data = pd.read_json(self._source_file_path)
        data['birthday'] = pd.to_datetime(data['birthday'])
        return data
