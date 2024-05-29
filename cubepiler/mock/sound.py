from loguru import logger


async def sound_start():
    logger.warning("mock sound start")


async def sound_stop():
    logger.warning("mock sound stop")
