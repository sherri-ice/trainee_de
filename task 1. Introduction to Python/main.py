from src.dao.dao import DAO
# мб использовать флаги как в яндехе?


if __name__ == "__main__":
    ...
    # check flags
    # здесь что-то типа если таблица не создана, то создать и загрузить туда все данные
    dao = DAO()
    print(dao.check_table_existence("Students"))

