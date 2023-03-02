import json


class EmailStorage:
    def __init__(self, email_config_path: str):
        with open(email_config_path) as json_config:
            self.__email_list = json.load(json_config)['emails_for_notification']

    @property
    def email_list(self):
        return self.__email_list
