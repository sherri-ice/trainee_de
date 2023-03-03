import json


class EmailStorage:
    def __init__(self, email_config_path: str):
        with open(email_config_path) as json_config:
            self.__email_list = json.load(json_config)['emails_for_notification']

    @property
    def email_list(self):
        return self.__email_list


class SchemaStorage:
    def __init__(self, schema_config_path: str):
        with open(schema_config_path) as json_config:
            self.__schema_config = json.load(json_config)['schema']

    @property
    def schema_config(self):
        return self.__schema_config
