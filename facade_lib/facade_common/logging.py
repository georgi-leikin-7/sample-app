import logging
import sys

from loguru import logger
from pydantic_settings import BaseSettings


class LoggerSettings(BaseSettings):
    """Logger settings"""

    log_level: str = "INFO"


class EndpointFilter(logging.Filter):  # skipcq
    """Endpoint Filter"""

    def filter(self, record: logging.LogRecord) -> bool:
        """Logger Filter"""
        return record.args and len(record.args) >= 3 and record.args[2] != "/healthz"


class InterceptHandler(logging.Handler):  # skipcq
    """
    Default handler from examples in loguru documentation.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        """
        The emit method is used to handle the logging process for a given log record.
        It takes the log record as a parameter and performs the following steps:
        """
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def format_record(record: dict) -> str:
    """
    Format a log record into a string using a given format.

    Args:
        record (dict): The log record to format.

    Returns:
        str: The formatted log record as a string.
    """
    # Preserve color formatting and message only
    format_string = "<level>{message}</level>"  # For message coloring

    # Add the timestamp, level, file, and line to metadata (not shown in the output)
    record["extra"]["timestamp"] = record["time"].strftime("%Y-%m-%d %H:%M:%S")
    record["extra"]["level"] = record["level"].name
    record["extra"]["file"] = record["file"].name  # Only the file name, not the full path
    record["extra"]["line"] = record["line"]  # Line number in the file

    # Optionally: Add a detailed exception if needed
    format_string += "\n{extra}"
    format_string += "\n{exception}"

    return format_string


def init_py_logger():
    """
    Initialize the Python logger for uvicorn.

    This method initializes the logger for uvicorn by removing all handlers from existing uvicorn loggers,
    replacing the handler for the default uvicorn logger with an InterceptHandler, and configuring the logger
    to send logs to the standard output with a specified level and format.
    """
    logger_settings = LoggerSettings()

    loggers = (logging.getLogger(name) for name in logging.root.manager.loggerDict if name.startswith("uvicorn."))
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    # set logs output, level and format
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": logger_settings.log_level,
                "format": format_record,
            }
        ]
    )
