from src.etl.etl import ETL
from src.object_helper.student_helper import StudentHelper
from src.object_helper.room_helper import RoomHelper

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--students_source_file',
    type=str,
    help="Path for students data.",
    required=True
)
parser.add_argument(
    '--rooms_source_file',
    type=str,
    help="Path for rooms data",
    required=True
)
parser.add_argument(
    '--export_result_type',
    type=str,
    choices=['json', 'xml'],
    help="File types for result file.",
    default='json'
)

args = parser.parse_args()


def showcase(student_source_path: str, room_source_path: str, export_result_type: str):
    student_helper = StudentHelper()
    student_helper.set_data_source(student_source_path)
    room_helper = RoomHelper()
    room_helper.set_data_source(room_source_path)

    etl = ETL([student_helper, room_helper])
    etl.extract()
    etl.load()

    etl.export_results(output_format=export_result_type)


if __name__ == "__main__":
    showcase(args.students_source_file, args.rooms_source_file, args.export_result_type)
