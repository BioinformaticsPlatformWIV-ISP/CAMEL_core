import logging

logger = logging.getLogger('camel')
DEFAULT_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def initialize_logging() -> None:
    """
    Initializes the logging.
    :return: None
    """
    if logger.hasHandlers():
        return

    # General logging level
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.addHandler(logging.NullHandler())


initialize_logging()
