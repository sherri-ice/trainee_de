import logging.config
import yaml
import logging


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonType):
    _logger = None

    def __init__(self):
        with open('logs/logger_config.yaml', 'r') as f:
            log_cfg = yaml.safe_load(f.read())
            logging.config.dictConfig(log_cfg)
            self._logger = logging.getLogger(__name__)
            self._logger.setLevel(logging.INFO)
            self._logger.info("Logger init...")

    def get_logger(self):
        return self._logger
