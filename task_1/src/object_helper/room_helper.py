import pandas as pd

from object_helper.base_object_helper import BaseObjectHelper


class RoomHelper(BaseObjectHelper):

    def __init__(self):
        super().__init__(object_name="Rooms", source_file_path="sample_data/rooms.json")

    @property
    def object_name(self) -> str:
        return self._object_name

    def set_data_source(self, path_to_file: str) -> None:
        self._source_file_path = path_to_file

    def load_data_to_df(self) -> pd.DataFrame:
        return pd.read_json(self._source_file_path)
