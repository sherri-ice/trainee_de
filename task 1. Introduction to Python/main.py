from src.dao.dao import StudentDAO, RoomsDAO, DAO
# мб использовать флаги как в яндехе?


if __name__ == "__main__":
    ...
    # check flags
    # здесь что-то типа если таблица не создана, то создать и загрузить туда все данные
    student_dao = StudentDAO()
    student_dao.upload_file("students.json")
    print(student_dao.get_students())

