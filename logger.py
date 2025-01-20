from logging import (
    Logger,
    getLogger,
    FileHandler,
    Formatter,
)


def get_logger(level: str, msg_format: str, filename: str) -> Logger:
    """
    Creates and sets logger for generating log messages in file.
    """
    logger = getLogger(__name__)
    logger.setLevel(level)
    handler = FileHandler(f'{filename}', mode='w')
    formatter = Formatter(msg_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
