"""Imports and initializes loggers to make pypeeve logger easy to use."""


import logging
from pypeeve.logger._logger import (PypeeveLogger,
                                    TimedRotatingPypeeveLogger,
                                    SizedRotatingPypeeveLogger,
                                    DEBUG,
                                    INFO,
                                    WARNING,
                                    ERROR,
                                    CRITICAL,
                                    FORMAT_SMALL,
                                    FORMAT_MEDIUM,
                                    FORMAT_LARGE)

def _get_logger(logger_class, logger_name):
    logging.setLoggerClass(logger_class)
    return logging.getLogger(logger_name)

logger = _get_logger(TimedRotatingPypeeveLogger, "timed_rotating")
basic_logger = _get_logger(PypeeveLogger, "basic")
timed_rotating_logger = _get_logger(TimedRotatingPypeeveLogger, "timed_rotating")
sized_rotating_logger = _get_logger(SizedRotatingPypeeveLogger, "sized_rotating")
