import logging


def cs_logger(name=__name__, level=logging.ERROR) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)

    logger.addHandler(handler)

    return logger
