import logging
from logging import getLogger

from data.constants import LOG_FILENAME


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        filename=LOG_FILENAME,
        filemode="w",
        encoding="utf-8",
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
    )
    logging.info("Logging initialized")


__all__ = ["setup_logging", "getLogger"]
