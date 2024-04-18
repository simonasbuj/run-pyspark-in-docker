import logging
from pythonjsonlogger import jsonlogger
import traceback


def setup_logging(logs_output_file, logger_name):

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = jsonlogger.JsonFormatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s", "%m-%d-%Y %H:%M:%S")

    # add logs to file
    file_logger = logging.FileHandler(logs_output_file, 'a')
    file_logger.setFormatter(formatter)
    logger.addHandler(file_logger)

    # add logs to terminal
    console_logger = logging.StreamHandler()
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)

    return logger


def log_traceback(logger, reason, error, throw_error=True):
    error_message = traceback.format_exc()
    logger.error(reason)
    logger.error(f"{error}")
    logger.error(f"{error_message}")

    if throw_error:
        raise Exception(f"ENDING RUN, BECAUSE {reason}")