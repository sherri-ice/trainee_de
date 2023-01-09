from dao import StudentDAO, RoomDAO
from room import Room

from typing import List, Dict


class HostelAPI:
    def __init__(self):
        self.student_dao = StudentDAO()
        self.room_dao = RoomDAO()

    def get_rooms(self, condition) -> Dict[Room, int]:
        return self.room_dao.get_rooms(condition=condition)

    def get_top_k_rooms(self, condition) -> List[Room]:
        ...

    # @decorator
    def get_top_5_rooms_by_the_smallest_age(self) -> List[Room]:
        ...

    # @decorator
    def get_top_5_rooms_by_the_biggest_age_diff(self) -> List[Room]:
        ...

    # @decorator
    def get_rooms_with_different_genders(self) -> List[Room]:
        ...
