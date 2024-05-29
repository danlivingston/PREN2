import asyncio

from loguru import logger

from cubepiler.testdata import config01, config02, config03, config04, config05


async def run_detection():
    logger.warning("mock run detection")
    await asyncio.sleep(3)
    return config01


async def warmupModels():
    logger.warning("mock model warmup")
    await asyncio.sleep(1)
