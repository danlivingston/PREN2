import os
import sys

from loguru import logger


def configure(name):
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Defaults to INFO if not set
    logger.remove(0)
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
    )
    logger.add(
        f"logs/{name}_{{time:YYYY-MM-DD}}.log",
        enqueue=True,
        level="TRACE",
        rotation="00:00",
        retention="10d",
    )
    logger.debug("configured logger")
