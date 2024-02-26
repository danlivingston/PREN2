from loguru import logger


def bar():
    logger.info("bar() executing")
    logger.debug("debugginggg")
    a = 4
    logger.debug(a)


# TODO: Delete this example
