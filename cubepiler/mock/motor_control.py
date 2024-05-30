import asyncio

from loguru import logger


async def zero_bed():
    logger.warning("moving mocked bed")
    await asyncio.sleep(1)


async def show_bed(minrpm=30, maxrpm=600, steps=4050):
    logger.warning("moving mocked bed")
    await asyncio.sleep(1)


async def zero_mag():
    logger.warning("moving mocked mag")
    await asyncio.sleep(1)


async def motor_stop():
    logger.warning("motor mock stop")
    await asyncio.sleep(1)


# action format (rotation_by, push_index)
async def execute_action(action):
    logger.warning(f"mock executing action: {action}")
    await asyncio.sleep(1)
