import logging
import os
from logging.handlers import RotatingFileHandler
import string

from app.internal.consts import LOG_LEVEL_ENV, LOGGER_NAME


def setup_handler(log_handler, log_level):
    log_handler.setLevel(log_level)
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    log_handler.setFormatter(formatter)


def get_log_level_from_env():
    return logging.getLevelName(os.getenv(LOG_LEVEL_ENV, 'INFO'))


def get_current_log_level():
    logger = logging.getLogger(LOGGER_NAME)
    return logging.getLevelName(logger.level)


def init_logger():
    log_level = get_log_level_from_env()
    file_handler = RotatingFileHandler("service.log",
                                       mode='a',
                                       maxBytes=5 * 1024 * 1024,
                                       backupCount=2,
                                       encoding='utf-8',
                                       delay=0)

    setup_handler(file_handler, log_level)

    stream_handler = logging.StreamHandler()
    setup_handler(stream_handler, log_level)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def log_error(error_text: string, error_code_recevied: int = 1):
    logger = logging.getLogger(LOGGER_NAME)
    logger.error(f"Code received: {error_code_recevied} #: {error_text}")


def log_info(info_text: string):
    logger = logging.getLogger(LOGGER_NAME)
    logger.info(info_text)


def log_warning(warning_code_received: int, warning_text: string):
    logger = logging.getLogger(LOGGER_NAME)
    logger.warning(f"Code received: {warning_code_received} #: {warning_text}")


def log_debug(debug_text: string):
    logger = logging.getLogger(LOGGER_NAME)
    logger.debug(debug_text)
