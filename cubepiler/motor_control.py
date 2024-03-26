from time import sleep

from loguru import logger

import asyncio


def rotate_shaft(unit):
    deg = unit * 30  # 30° per unit / index
    logger.debug(f"rotating shaft by {deg} degrees")


def push_cube(index):
    logger.debug(f"pushing cube at position {index + 1}")


async def execute_action(action):
    rotate_by, push_index = action
    rotate_shaft(rotate_by)
    push_cube(push_index)

    await asyncio.sleep(0.5)  # TODO: remove


async def execute_actions(actions, q=asyncio.Queue()):
    logger.debug(f"executing actions {actions}")

    base = 55
    buffer = 5
    step = (100 - base - buffer) / len(actions)
    curr = 0

    logger.debug(f"{base} {buffer} {step} {curr}")

    for action in actions:
        logger.debug(f"executing action {action}")

        curr += 1
        percent = base + curr * step
        logger.debug(f"{percent}")
        await q.put((percent, f"placing {curr}/{len(actions)} cubes"))

        await execute_action(action)
