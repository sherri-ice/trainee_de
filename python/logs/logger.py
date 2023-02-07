from __future__ import annotations

import logging.config

import yaml


class SingletonType(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        """
        The __call__ function is a builtin function that you can call from an instance of a class.
        It allows you to treat the object like a function, so instead of calling my_class(),
        you can call my_class.__call__(). This is useful if you want to make sure that only one instance
        of your class ever exists.

        :param cls: Call the __init__ method of the class
        :param *args: Pass a non-keyworded, variable-length argument list
        :param **kwargs: Pass keyworded variable length of arguments to a function
        :return: The instance of the class
        """
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Logger(metaclass=SingletonType):

    def __init__(self):
        """
        Logger for ETL process.

        :param self: Access variables that belongs to the class
        :return: None
        """
        try:
            with open('logs/logger_config.yaml') as f:
                log_cfg = yaml.safe_load(f.read())
                logging.config.dictConfig(log_cfg)
        except FileNotFoundError:
            self._logger = logging.getLogger(__name__)
            self._logger.setLevel(logging.INFO)
            self._logger.warning(
                'Config for logger not found, consider to take default logger...',
            )
            return
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        self._logger.info('Logger init...')

    def get_logger(self) -> Logger:
        """
        The get_logger function returns the logger instance created by the
        constructor. Important notice: Logger uses Singleton pattern to prevent multiple instances in different modules.
         This is helpful for cases where multiple modules need to log events.

        :param self: Reference the class instance itself
        :return: Logger object
        """
        return self._logger
