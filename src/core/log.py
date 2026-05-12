# myapp.py
import logging

from src.core.config import LOGGER_NAME, LOGGER_PATH, LOGGER_FORMAT

logger = logging.getLogger(LOGGER_NAME)
logging.basicConfig(format=LOGGER_FORMAT, filename=LOGGER_PATH)


if __name__ == "__main__":
    # run with: python -m src.core.log
    logger = logging.getLogger(LOGGER_NAME)
    logger.info("logger test passed.")
    logger.error("occurs an error.")
