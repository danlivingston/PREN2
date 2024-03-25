from time import sleep
from loguru import logger


def rotate_shaft(unit):
    deg = unit * 30  # 30° per unit / index
    logger.debug(f"rotating shaft by {deg} degrees")


def push_cube(index):
    logger.debug(f"pushing cube at position {index + 1}")


def execute_action(action):
    rotate_by, push_index = action
    rotate_shaft(rotate_by)
    push_cube(push_index)

    sleep(0.5)  # TODO: remove


def execute_actions(actions):
    logger.debug(f"executing actions {actions}")
    for action in actions:
        logger.debug(f"executing action {action}")
        execute_action(action)
