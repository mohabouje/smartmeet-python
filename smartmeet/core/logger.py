import logging
from singleton_decorator import singleton


@singleton
class Logger:
    def __init__(self):
        self.__level = logging.DEBUG
        self.__loggers = dict()
        
    def __get_logger(self, logger_name) -> logging.Logger:
        if logger_name not in self.__loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(self.__level)
            self.__loggers[logger_name] = logger
        return self.__loggers[logger_name]

    def debug(self, msg: str, logger_name: str = "root"):
        self.__get_logger(logger_name).debug(msg)

    def error(self, msg: str, logger_name: str = "root"):
        self.__get_logger(logger_name).error(msg)

    def info(self, msg: str, logger_name: str = "root"):
        self.__get_logger(logger_name).info(msg)

    def warning(self, msg: str, logger_name: str = "root"):
        self.__get_logger(logger_name).warning(msg)

    @property
    def level(self):
        return self.level

    @level.setter
    def level(self, level):
        self.__level = level
        for logger in self.__loggers:
            logger.setLevel(level)
