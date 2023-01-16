import pandas as pd

from object_helper.base_object_helper import BaseObjectHelper


class RoomHelper(BaseObjectHelper):

    def __init__(self, source_file_path="sample_data/rooms.json"):
        super().__init__(object_name="Rooms", source_file_path=source_file_path)

    @property
    def object_name(self) -> str:
        return self._object_name

    def load_data_to_df(self) -> pd.DataFrame:
        super().load_data_to_df()
        return pd.read_json(self._source_file_path)
