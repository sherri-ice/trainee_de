import json


class DBConfigHelper:
    def __init__(self, config_path: str = "configs/db_config.json"):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            self._db_host = config['db_host']
            self._db_type = config['db_type']
            self._db_username = config['db_username']
            self._db_password = config['db_password']
            self._db_name = config['db_name']
            self._db_port = config['db_port']

    def get_credentials(self) -> str:
        return f'{self._db_type}://' \
               f'{self._db_username}:{self._db_password}@{self._db_host}:{self._db_port}/{self._db_name}'

    def get_config(self):
        return {
            'host': self._db_host,
            'database': self._db_name,
            'user': self._db_username,
            'password': self._db_password,
            'port': self._db_port
        }



