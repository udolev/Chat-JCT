import logging
import os

from app.internal.consts import LOG_LEVEL_ENV
from app.internal.infra_logger import get_log_level_from_env


def test_default_log_level():
    if LOG_LEVEL_ENV in os.environ:
        del os.environ[LOG_LEVEL_ENV]

    assert get_log_level_from_env() == logging.INFO


def test_non_default_log_level():
    os.environ[LOG_LEVEL_ENV] = 'DEBUG'
    assert get_log_level_from_env() == logging.DEBUG

