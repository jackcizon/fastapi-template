import os
from logging import config

from src.core.config import ROOT_DIR, settings


def setup_logging() -> None:
    log_dir = os.path.join(ROOT_DIR, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    config.dictConfig(settings.log)
