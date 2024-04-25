import asyncio
import os
import time
from datetime import datetime
from enum import Enum

from loguru import logger

GPIO = None
try:
    import RPi.GPIO as GPIO
except:
    from cubepiler import GPIO_mock as GPIO


from cubepiler.DRV8825 import DRV8825

Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor1.SetMicroStep("hardward", "1/4step")
Motor2.SetMicroStep("hardward", "1/4step")
Motor1.Stop()
Motor2.Stop()

endschalter = 8
channelX = 10

sole1 = 14
sole2 = 23
sole3 = 25
sole4 = 9


masterposition = 0


def GPIO_setup():
    GPIO.setup(endschalter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(channelX, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sole1, GPIO.OUT)
    GPIO.setup(sole2, GPIO.OUT)
    GPIO.setup(sole3, GPIO.OUT)
    GPIO.setup(sole4, GPIO.OUT)


GPIO_setup()


class Magpositions(Enum):
    magA = 0
    magB = 1066
    magC = 2133


class Platepositions(Enum):
    plate1 = 0
    plate2 = 800
    plate3 = 1600
    plate4 = 2400


def zero_bed():
    while GPIO.input(endschalter) == 0:
        Motor2.TurnStep(Dir="backward", steps=1, stepdelay=0.00005)
    Motor2.Stop()
    return ()


def show_bed():
    Motor2.TurnStep(Dir="forward", steps=9000, stepdelay=0.00005)
    Motor2.Stop()
    return ()


def zero_mag():
    global masterposition
    while GPIO.input(channelX) == 0:
        Motor1.TurnStep(Dir="forward", steps=1, stepdelay=0.00005)
    Motor1.TurnStep(Dir="forward", steps=250, stepdelay=0.00005)
    time.sleep(0.2)
    Motor1.Stop()
    masterposition = 0
    return ()


def place_cube(mag, pos):
    global masterposition

    actualpos = masterposition + mag
    if actualpos >= 3200:
        actualpos -= 3200

    schritte = pos - actualpos
    if schritte < 0:
        schritte = 3200 - abs(schritte)

    Motor1.TurnStep(Dir="forward", steps=schritte, stepdelay=0.00005)

    if pos == 0:
        GPIO.output(sole1, 1)
        time.sleep(0.1)
        GPIO.output(sole1, 0)
    elif pos == 800:
        GPIO.output(sole2, 1)
        time.sleep(0.1)
        GPIO.output(sole2, 0)
    elif pos == 1600:
        GPIO.output(sole3, 1)
        time.sleep(0.1)
        GPIO.output(sole3, 0)
    elif pos == 2400:
        GPIO.output(sole4, 1)
        time.sleep(0.1)
        GPIO.output(sole4, 0)

    time.sleep(0.1)
    masterposition += schritte
    if masterposition >= 3200:
        masterposition -= 3200
    return ()


# GPIO.setmode(GPIO.BCM)

# ShaftMotor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
# ShaftMotor.SetMicroStep("hardward", "1/4step")
# ShaftMotorSpeed = os.getenv("SHAFTMOTOR_SPEED", 0.00005)

# PlatformMotor = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
# PlatformMotor.SetMicroStep("hardward", "1/4step")
# PlatformMotorSpeed = os.getenv("PLATFORMMOTOR_SPEED", 0.00005)
# PlatformTopPin = 8
# GPIO.setup(PlatformTopPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def rotate_shaft(unit):
    deg = unit * 30  # 30° per unit / index
    logger.debug(f"rotating shaft by {deg} degrees")
    # TODO: implement


def push_cube(index):
    logger.debug(f"pushing cube at position {index + 1}")
    # TODO: implement


def testFunctions():
    GPIO_setup()
    zero_bed()
    zero_mag()
    place_cube(Magpositions.magA.value, Platepositions.plate2.value)
    place_cube(Magpositions.magA.value, Platepositions.plate1.value)
    place_cube(Magpositions.magC.value, Platepositions.plate1.value)
    place_cube(Magpositions.magC.value, Platepositions.plate4.value)
    place_cube(Magpositions.magB.value, Platepositions.plate3.value)
    place_cube(Magpositions.magB.value, Platepositions.plate4.value)
    place_cube(Magpositions.magA.value, Platepositions.plate2.value)
    place_cube(Magpositions.magA.value, Platepositions.plate3.value)
    Motor1.Stop()
    show_bed()
    GPIO.cleanup()


# action format (rotation_by, push_index)
async def execute_action(action):
    rotate_by, push_index = action
    rotate_shaft(rotate_by)
    push_cube(push_index)

    await asyncio.sleep(0.5)  # TODO: remove fake delay


# def reset_platform_position():
#     pass
# done = False

# while not done:
#     PlatformMotor.TurnStep(Dir="forward", steps=1, stepdelay=PlatformMotorSpeed)
#     done = GPIO.input(PlatformTopPin)
