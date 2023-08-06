import os
import logging
from datetime import datetime

from src.mb_cruise_migration.framework.consts.log_level_consts import LogLevels


class LoggerBuilder(object):
    def __init__(self, keyword, level, handler, formatter):
        self.__formatter = formatter
        self.__handler = handler
        self.__level = level
        self.__logger: logging.Logger = logging.getLogger(f'{keyword}')

        self.__remove_existing_handlers()
        self.__add_handler_to_logger()
        self.__set_logger_level()

    def get_logger(self):
        return self.__logger

    @staticmethod
    def create_log_file_path(log_root: str, log_dir, keyword):
        if not log_root:
            log_root = os.getcwd()
        dirpath = os.path.join(log_root, log_dir)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        timestamp = datetime.now().strftime('%y-%m-%d_%H%M%S')
        return os.path.join(dirpath, f'{keyword}_{timestamp}.log')

    def __get_formatter(self):
        return self.__formatter

    def __remove_existing_handlers(self):
        handlers = self.__logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.__logger.removeHandler(handler)

    def __add_handler_to_logger(self):
        self.__handler.setFormatter(self.__get_formatter())
        self.__logger.addHandler(self.__handler)

    def __set_logger_level(self):
        level = self.__level
        if level == LogLevels.INFO:
            self.__logger.setLevel(logging.INFO)
        elif level == LogLevels.WARNING:
            self.__logger.setLevel(logging.WARNING)
        elif level == LogLevels.CRITICAL:
            self.__logger.setLevel(logging.CRITICAL)
        else:
            self.__logger.setLevel(logging.DEBUG)
