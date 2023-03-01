from __future__ import annotations

import json


class DBConfigHelper:
    def __init__(self, config_path: str = 'sql_helper/configs/db_config.json'):
        """
        DBCongigHelper helps to load databases configuration from JSON files.


        :param self: Reference the current instance of the class
        :param config_path:str='sql_helper/configs/db_config.json': Specify the path to the database configuration file
        :return: None
        """
        with open(config_path) as config_file:
            config = json.load(config_file)
            self._db_host = config['db_host']
            self._db_type = config['db_type']
            self._db_username = config['db_username']
            self._db_password = config['db_password']
            self._db_name = config['db_name']
            self._db_port = config['db_port']

    def get_credentials(self) -> str:
        """
        The get_credentials function returns a string containing the database credentials.
        The function is used to create a connection string for the SQLAlchemy engine.

        :param self: Access the attributes and methods of the class
        :return: A string of the credentials for the database
        """
        return f'{self._db_type}://' \
               f'{self._db_username}:{self._db_password}@{self._db_host}:{self._db_port}/{self._db_name}'
