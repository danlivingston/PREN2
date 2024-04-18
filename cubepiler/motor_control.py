import asyncio
import os

from loguru import logger

from cubepiler.utils import is_raspberrypi

GPIO = None
if is_raspberrypi():
    import RPi.GPIO as GPIO
else:
    from cubepiler import GPIO_mock as GPIO

from cubepiler.DRV8825 import DRV8825

GPIO.setmode(GPIO.BCM)

ShaftMotor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
ShaftMotor.SetMicroStep("hardward", "1/4step")
ShaftMotorSpeed = os.getenv("SHAFTMOTOR_SPEED", 0.00005)

PlatformMotor = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
PlatformMotor.SetMicroStep("hardward", "1/4step")
PlatformMotorSpeed = os.getenv("PLATFORMMOTOR_SPEED", 0.00005)
PlatformTopPin = 8
GPIO.setup(PlatformTopPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


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


def reset_platform_position():
    done = False

    while not done:
        PlatformMotor.TurnStep(Dir="forward", steps=1, stepdelay=PlatformMotorSpeed)
        done = GPIO.input(PlatformTopPin)
