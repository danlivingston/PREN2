import asyncio

from loguru import logger


async def start_detection():
    logger.warning("mock start detection")
    await asyncio.sleep(2)


async def warmupModels():
    logger.warning("mock model warmup")
    await asyncio.sleep(1)
