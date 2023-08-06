"""Custom logger to make logging easy"""


import os
import logging
from logging import handlers
import functools
import time
from typing import Any


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

FORMAT_SMALL = '[%(asctime)s] '\
                + '- [%(levelname)s] '\
                + '- %(message)s'
FORMAT_MEDIUM = '[%(asctime)s] '\
                + '- [%(module)s] '\
                + '- [%(funcName)s] '\
                + '- [%(lineno)d] '\
                + '- [%(levelname)s] '\
                + '- %(message)s'
FORMAT_LARGE = '[%(asctime)s] '\
                + '- [%(module)s] '\
                + '- [%(funcName)s] '\
                + '- [%(lineno)d] '\
                + '- [%(thread)d] '\
                + '- [%(process)d] '\
                + '- [%(levelname)s] '\
                + '- %(message)s'


class PypeeveLogger(logging.Logger):
    """A custom basic logger that provides an easy way to create a logger
    with little to no update in the config.

    ### Examples
    Here is how you can use the pre-configured `logger`

    ```python
    from pypeeve.logger import logger
    logger.info("Info logs")
    logger.error("Error logs")
    ```

    To use the `basic_logger`

    ```python
    from pypeeve.logger import basic_logger as logger
    logger.debug("Debug logs")
    logger.critical("Critical logs")
    ```

    Similarly, to use the `sized_rotating_logger`

    ```python
    from pypeeve.logger import sized_rotating_logger as logger
    logger.info("Info logs")
    logger.warning("Warning logs")
    ```

    If you wish to change the log type or log format, you can do
    it using `update_loglevel()` and `update_logformat()` methods.
    We recommend to update the level and format to the module which
    will be called first when you start your application so that
    all the other modules that import the logger get the updated setting.

    ```python
    from pypeeve.logger import logger, DEBUG, FORMAT_MEDIUM
    logger.update_loglevel(DEBUG)
    logger.update_logformat(FORMAT_MEDIUM)

    logger.debug("Debug logs")
    ```


    ### Pypeeve Logger Decorators
    Pypeeve logger provides two decorator at this moment-

    `default` is a decorator to log the entry and exit of a function.

    `perf` is a decorator to log the total time to execute a function.

    ```python
    from pypeeve.logger import logger

    @logger.default
    @logger.perf
    def do_something():
        logger.info("Info logs")
        logger.error("Error logs")
    ```


    ### Create Customized Logger

    To create a logger with custom configuration, all you need to do is
    to import your desired types of Logger class- `PypeeveLogger`,
    `TimedRotatingPypeeveLogger` or `SizedRotatingPypeeveLogger`.

    ```python
    # mylogger.py
    from pypeeve.logger import PypeeveLogger, DEBUG
    logger = PypeeveLogger(level=DEBUG
    ```

    Once the logger is create, it's ready to be imported and used.

    ```python
    # other_module.py
    from mylogger import logger
    logger.info("Info logs")
    ```
    """
    def __init__(self,
                name: str="basic",
                level: int=INFO,
                logformat: str=FORMAT_MEDIUM,
                filepath: str="logs/pypeeve.log") -> None:
        """A custom basic logger

        Args:
            name (str, optional): A name of the logger. Defaults to "basic".
            level (int, optional): Log level of the logger. Defaults to INFO.
            logformat (str, optional): Format of the logger. Defaults to
            FORMAT_MEDIUM.
            filepath (str, optional): File path to store the logs. Defaults
            to "logs/pypeeve.log".
        """

        super().__init__(name=name, level=level)

        self.name = name
        self.logformat = logformat
        self.filepath = filepath
        self.custom_handlers = []
        self.__setup()

    def __setup(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        self.setLevel(level=self.level)
        formatter = logging.Formatter(self.logformat)
        self.custom_handlers.append(self._create_stream_handler())
        self.custom_handlers.append(self._create_file_handler())
        self.__setup_handlers(formatter)

    def _create_stream_handler(self):
        return logging.StreamHandler()

    def _create_file_handler(self):
        return logging.FileHandler(filename=self.filepath)

    def __setup_handlers(self, formatter: logging.Formatter) -> None:
        for handler in self.custom_handlers:
            handler.setFormatter(formatter)
            self.addHandler(handler)

    def update_logformat(self, logformat: str) -> None:
        """Update the log format in runtime.

        Args:
            logformat (str): A custom log format
        """
        formatter = logging.Formatter(logformat)
        for handler in self.custom_handlers:
            handler.setFormatter(formatter)

    def update_loglevel(self, loglevel: Any) -> None:
        """Update the log level in runtime.

        Args:
            loglevel (Any): A log level to set
        """
        self.setLevel(loglevel)

    def default(self, function: Any) -> Any:
        """A decorator to log the entry and exit of a function.

        Args:
            function (Any): A function that is wrapped in decorator.
        """

        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            self.__update_record(record, function)
            return record

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            logging.setLogRecordFactory(record_factory)
            self.debug("Entering %s%s", function.__name__, "()")
            logging.setLogRecordFactory(old_factory)

            value = function(*args, **kwargs)

            logging.setLogRecordFactory(record_factory)
            self.debug("Exiting %s%s", function.__name__, "()")
            logging.setLogRecordFactory(old_factory)

            return value

        return wrapper

    def perf(self, function: Any) -> Any:
        """A decorator to log the total time to execute a function.

        Args:
            function (Any): A function that is wrapped in decorator.
        """

        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            self.__update_record(record, function)
            return record

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            start_time = round(time.perf_counter(), 6)
            value = function(*args, **kwargs)
            end_time = round(time.perf_counter(), 6)
            total_time = round(end_time - start_time, 6)

            logging.setLogRecordFactory(record_factory)
            self.debug("%s%s starting time: %s",
                       function.__name__,
                       "()",
                       str(start_time))
            self.debug("%s%s ending time: %s",
                       function.__name__,
                       "()",
                       str(end_time))
            self.info("Total time taken to finish %s%s: %s %s",
                      function.__name__,
                      "()",
                      str(total_time),
                      "second(s)")
            logging.setLogRecordFactory(old_factory)

            return value

        return wrapper

    def __update_record(self, record: Any, function: Any) -> None:
        record.pathname = function.__globals__['__file__']
        record.module = function.__module__.split('.')[-1]
        record.funcName = function.__name__
        record.lineno = -1


class TimedRotatingPypeeveLogger(PypeeveLogger):
    """A custom logger that provides an easy way to create a timed
    rotating logger with little to no update in the config.

    ### Examples
    Here is how you can use the pre-configured `logger`

    ```python
    from pypeeve.logger import logger
    logger.info("Info logs")
    logger.error("Error logs")
    ```

    To use the `basic_logger`

    ```python
    from pypeeve.logger import basic_logger as logger
    logger.debug("Debug logs")
    logger.critical("Critical logs")
    ```

    Similarly, to use the `sized_rotating_logger`

    ```python
    from pypeeve.logger import sized_rotating_logger as logger
    logger.info("Info logs")
    logger.warning("Warning logs")
    ```

    If you wish to change the log type or log format, you can do
    it using `update_loglevel()` and `update_logformat()` methods.
    We recommend to update the level and format to the module which
    will be called first when you start your application so that
    all the other modules that import the logger get the updated setting.

    ```python
    from pypeeve.logger import logger, DEBUG, FORMAT_MEDIUM
    logger.update_loglevel(DEBUG)
    logger.update_logformat(FORMAT_MEDIUM)

    logger.debug("Debug logs")
    ```


    ### Pypeeve Logger Decorators
    Pypeeve logger provides two decorator at this moment-

    `default` is a decorator to log the entry and exit of a function.

    `perf` is a decorator to log the total time to execute a function.

    ```python
    from pypeeve.logger import logger

    @logger.default
    @logger.perf
    def do_something():
        logger.info("Info logs")
        logger.error("Error logs")
    ```


    ### Create Customized Logger

    To create a logger with custom configuration, all you need to do is
    to import your desired types of Logger class- `PypeeveLogger`,
    `TimedRotatingPypeeveLogger` or `SizedRotatingPypeeveLogger`.

    ```python
    # mylogger.py
    from pypeeve.logger import TimedRotatingPypeeveLogger, DEBUG
    logger = TimedRotatingPypeeveLogger(level=DEBUG, backup_count=20)
    ```

    Once the logger is create, it's ready to be imported and used.

    ```python
    # other_module.py
    from mylogger import logger
    logger.info("Info logs")
    ```
    """

    def __init__(self,
                 name: str = "timed_rotating",
                 level: int = INFO,
                 logformat: str = FORMAT_LARGE,
                 filepath: str = "logs/pypeeve.log",
                 when_to_rotate: str="midnight",
                 backup_count: int=10) -> None:
        """A custom timed rotating logger

        Args:
            name (str, optional): A name of the logger. Defaults to
            "timed_rotating".
            level (int, optional): Log level of the logger. Defaults to INFO.
            logformat (str, optional): Format of the logger. Defaults to
            FORMAT_MEDIUM.
            filepath (str, optional): File path to store the logs. Defaults
            to "logs/pypeeve.log".
            when_to_rotate (str, optional): Specify when to rollover logfile.
            Defaults to "midnight".
            backup_count (int, optional): Number of backup logfiles. Defaults
            to 10.
        """
        self.when_to_rotate = when_to_rotate
        self.backup_count = backup_count
        super().__init__(name, level, logformat, filepath)

    def _create_file_handler(self):
        return handlers.TimedRotatingFileHandler(filename=self.filepath,
                                                when=self.when_to_rotate,
                                                backupCount=self.backup_count)


class SizedRotatingPypeeveLogger(PypeeveLogger):
    """A custom logger that provides an easy way to create a sized
    rotating logger with little to no update in the config.

    ### Examples
    Here is how you can use the pre-configured `logger`

    ```python
    from pypeeve.logger import logger
    logger.info("Info logs")
    logger.error("Error logs")
    ```

    To use the `basic_logger`

    ```python
    from pypeeve.logger import basic_logger as logger
    logger.debug("Debug logs")
    logger.critical("Critical logs")
    ```

    Similarly, to use the `sized_rotating_logger`

    ```python
    from pypeeve.logger import sized_rotating_logger as logger
    logger.info("Info logs")
    logger.warning("Warning logs")
    ```

    If you wish to change the log type or log format, you can do
    it using `update_loglevel()` and `update_logformat()` methods.
    We recommend to update the level and format to the module which
    will be called first when you start your application so that
    all the other modules that import the logger get the updated setting.

    ```python
    from pypeeve.logger import logger, DEBUG, FORMAT_MEDIUM
    logger.update_loglevel(DEBUG)
    logger.update_logformat(FORMAT_MEDIUM)

    logger.debug("Debug logs")
    ```


    ### Pypeeve Logger Decorators
    Pypeeve logger provides two decorators at this moment-

    `default` is a decorator to log the entry and exit of a function.

    `perf` is a decorator to log the total time to execute a function.

    ```python
    from pypeeve.logger import logger

    @logger.default
    @logger.perf
    def do_something():
        logger.info("Info logs")
        logger.error("Error logs")
    ```


    ### Create Customized Logger

    To create a logger with custom configuration, all you need to do is
    to import your desired types of Logger class- `PypeeveLogger`,
    `TimedRotatingPypeeveLogger` or `SizedRotatingPypeeveLogger`.

    ```python
    # mylogger.py
    from pypeeve.logger import SizedRotatingPypeeveLogger, DEBUG
    logger = SizedRotatingPypeeveLogger(level=DEBUG, backup_count=20)
    ```

    Once the logger is create, it's ready to be imported and used.

    ```python
    # other_module.py
    from mylogger import logger
    logger.info("Info logs")
    ```
    """

    def __init__(self,
                 name: str = "sized_rotating",
                 level: int = INFO,
                 logformat: str = FORMAT_LARGE,
                 filepath: str = "logs/pypeeve.log",
                 max_bytes: int = 10000000,
                 backup_count: int=10) -> None:
        """A custom sized rotating logger

        Args:
            name (str, optional): A name of the logger. Defaults to
            "sized_rotating".
            level (int, optional): Log level of the logger. Defaults to INFO.
            logformat (str, optional): Format of the logger. Defaults to
            FORMAT_MEDIUM.
            filepath (str, optional): File path to store the logs. Defaults
            to "logs/pypeeve.log".
            max_bytes (int, optional): Maximum size of the logfile. Defaults
            to 10000000 bytes (~10 MB).
            backup_count (int, optional): Number of backup logfiles. Defaults
            to 10.
        """
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        super().__init__(name, level, logformat, filepath)

    def _create_file_handler(self):
        return handlers.RotatingFileHandler(filename=self.filepath,
                                            maxBytes=self.max_bytes,
                                            backupCount=self.backup_count)
