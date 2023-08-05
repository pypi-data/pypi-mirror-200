import logging
import os
from datetime import datetime

import inspect
from pathlib import Path


# Create an enum of log levels
from enum import Enum
from typing import Optional

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    NONE = 0


def setup_logging(log_name: Optional[str] = None, file_level: LogLevel = LogLevel.NONE, console_level: LogLevel = LogLevel.DEBUG, simple_fmt: bool = False) -> logging.Logger:

    if log_name is None:
        frame = inspect.stack()
        if len(frame) <= 1:
            log_name = __name__
        else:
            caller_frame = frame[1]
            caller_path = caller_frame.filename
            # Get the stem of filename of call_path
            file_path = Path(caller_path)
            file_stem = file_path.stem
            log_name = file_stem

    # Create a logger with the name of your project
    logger = logging.getLogger(f"{log_name}")
    list(map(logger.removeHandler, logger.handlers))
    list(map(logger.removeFilter, logger.filters))

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Create a formatter
    if simple_fmt:
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s - %(message)s")
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(process)s - %(message)s")


    # Create a console handler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level.value)

    # Add the formatter to the file and console handlers
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)

    if (file_level != LogLevel.NONE):
        # Get current date and time
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        # Create log file name with current date and time
        log_name = log_name + '_' + current_time + '.log'

        # Create a file handler to log to a file
        log_path = os.path.join(os.getcwd(), 'logs', log_name)
        # Create the logs directory if it doesn't exist
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        file_handler = logging.FileHandler(log_name)
        file_handler.setLevel(file_level.value)

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.propagate = False

    return logger
