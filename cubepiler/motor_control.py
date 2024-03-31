import asyncio

from loguru import logger


def rotate_shaft(unit):
    deg = unit * 30  # 30° per unit / index
    logger.debug(f"rotating shaft by {deg} degrees")
    # TODO: implement


def push_cube(index):
    logger.debug(f"pushing cube at position {index + 1}")
    # TODO: implement


# action format (rotation_by, push_index)
async def execute_action(action):
    rotate_by, push_index = action
    rotate_shaft(rotate_by)
    push_cube(push_index)

    await asyncio.sleep(0.5)  # TODO: remove fake delay
