import json


class EmailStorage:
    """Class which loads recipients emails from json file"""
    def __init__(self, email_config_path: str):
        with open(email_config_path) as json_config:
            self.__email_list = json.load(json_config)['emails_for_notification']

    @property
    def email_list(self):
        return self.__email_list
