# coding: utf-8
# stb lib
import logging
import os
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

# our own lib
from conf.config import log_conf
from json_formatter import JSONFormatter


def init_logger(service="default_service", logger_name='all'):
    if logger_name not in Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_conf['level'])
        # file
        fmt = '%(asctime)s - %(process)s - %(levelname)s: - %(message)s'
        formatter = logging.Formatter(fmt)

        # all file
        log_file = os.path.join(log_conf['log_dir'], logger_name + '.log')
        file_handler = TimedRotatingFileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # error file
        log_file = os.path.join(log_conf['log_dir'],
                                logger_name + '.error.log')
        file_handler = TimedRotatingFileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.ERROR)
        logger.addHandler(file_handler)

        # 以JSON格式打印，以供rsyslog 收集，最终落地到ES
        formatter = JSONFormatter(service)
        log_file = os.path.join(log_conf['log_dir'], logger_name + '_json.log')
        file_handler = TimedRotatingFileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger = logging.getLogger(logger_name)
    return logger
