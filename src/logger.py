import logging
import os

from logging.handlers import RotatingFileHandler


class Logger:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_dir='log'):
        self.log_dir = log_dir

        os.makedirs(self.log_dir, exist_ok=True)

        self.info_log = os.path.join(self.log_dir, "activity.log")
        self.error_log = os.path.join(self.log_dir, "errors.log")

        info_handler = RotatingFileHandler(filename=self.info_log, maxBytes=5 * 1024 * 1024, backupCount=3,
                                           encoding='utf-8')
        error_handler = RotatingFileHandler(filename=self.error_log, maxBytes=2 * 1024 * 1024, backupCount=5,
                                            encoding='utf-8')

        info_handler.setLevel(logging.INFO)
        error_handler.setLevel(logging.ERROR)

        log_format = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
                                       datefmt='%Y-%m-%d %H:%M:%S')

        info_handler.setFormatter(log_format)
        error_handler.setFormatter(log_format)

        self.logger = logging.getLogger("StudentSystem")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            self.logger.addHandler(info_handler)
            self.logger.addHandler(error_handler)

            console_formatter = logging.Formatter('%(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)
