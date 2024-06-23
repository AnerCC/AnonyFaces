import logging
from logging.handlers import RotatingFileHandler

def create_logger(name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Create a console handler and set its level to INFO
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)

    # Create a file handler and set its level to DEBUG
    max_log_size = 8 * 1024 * 1024
    log_file=(f'{name}.log')
    file_handler =RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger



