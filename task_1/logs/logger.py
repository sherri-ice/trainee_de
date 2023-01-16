from __future__ import annotations

import logging.config

import yaml


class SingletonType(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Logger(metaclass=SingletonType):
    _logger = None

    def __init__(self):
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

    def get_logger(self):
        return self._logger
