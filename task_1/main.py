
# мб использовать флаги как в яндехе?
from src.etl.etl import ETL
from src.object_helper.student_helper import StudentHelper
from src.object_helper.room_helper import RoomHelper

if __name__ == "__main__":
    student_helper = StudentHelper()
    room_helper = RoomHelper()

    etl = ETL([student_helper, room_helper])
    etl.extract()
    etl.load()
    print(etl.select_rooms_with_different_gender())


