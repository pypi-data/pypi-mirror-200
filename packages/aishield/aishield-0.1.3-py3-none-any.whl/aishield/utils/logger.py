import logging
from logging import Logger


def getLogger(name: str) -> Logger:
    logger: Logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # create console handler and set level to info
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    # create formatter for console handler
    c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # add formatter to c_handler
    c_handler.setFormatter(c_format)
    # add c_handler to logger
    logger.addHandler(c_handler)
    return logger
