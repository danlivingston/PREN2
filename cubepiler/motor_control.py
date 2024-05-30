import asyncio
import time
from enum import Enum

import RPi.GPIO as GPIO
from loguru import logger

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
sole3 = 9  # 4
sole4 = 25  # 3


masterposition = 0


def GPIO_setup():
    GPIO.setup(endschalter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(channelX, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sole1, GPIO.OUT)
    GPIO.setup(sole2, GPIO.OUT)
    GPIO.setup(sole3, GPIO.OUT)
    GPIO.setup(sole4, GPIO.OUT)


GPIO_setup()


def GPIO_cleanup():
    GPIO.output(sole1, 0)
    GPIO.output(sole2, 0)
    GPIO.output(sole3, 0)
    GPIO.output(sole4, 0)

    GPIO.output(18, 0)
    GPIO.output(19, 0)
    GPIO.output(12, 0)
    GPIO.output(4, 0)


class Magpositions(Enum):
    magA = 0
    magB = 1066
    magC = 2133


class Platepositions(Enum):
    plate1 = 0
    plate2 = 800
    plate3 = 1600
    plate4 = 2400


async def zero_bed():
    while GPIO.input(endschalter) == 0:
        Motor2.TurnStep(Dir="backward", steps=1, stepdelay=0.0005)
    asyncio.sleep(0.1)
    Motor2.TurnStep(Dir="forward", steps=150, stepdelay=0.0005)

    Motor2.Stop()
    return ()


async def show_bed(minrpm=30, maxrpm=600, steps=4050):
    maxsteps = steps
    actualsteps = 0
    acceltime = 0.2

    linkoeff = (maxrpm - minrpm) / acceltime
    # timestamp = 0
    targetrpm = minrpm

    while (targetrpm < maxrpm) & (actualsteps < maxsteps):
        delay = 60 / (2 * 200 * targetrpm)
        Motor2.TurnStep(Dir="forward", steps=1, stepdelay=delay)
        actualsteps += 1

        targetrpm += linkoeff * (2 * delay)

    print("Endgeschwindigkeit erreicht")

    delayfix = 60 / (2 * 200 * maxrpm)
    # stepsfix = int(1 / (2 * delayfix))
    while actualsteps < maxsteps:
        Motor2.TurnStep(Dir="forward", steps=1, stepdelay=delayfix)
        actualsteps += 1

    Motor2.Stop()

    return ()


async def zero_mag():
    global masterposition
    while GPIO.input(channelX) == 0:
        Motor1.TurnStep(Dir="forward", steps=1, stepdelay=0.00005)
    Motor1.TurnStep(Dir="forward", steps=210, stepdelay=0.00005)
    time.sleep(0.2)
    Motor1.Stop()
    masterposition = 0
    return ()


async def place_cube(mag, pos):
    global masterposition

    actualpos = masterposition + mag
    if actualpos >= 3200:
        actualpos -= 3200

    schritte = pos - actualpos
    if schritte < 0:
        schritte = 3200 - abs(schritte)

    logger.debug(f"schritte berechnet: {schritte}")
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


async def motor_stop():
    Motor1.Stop()


# action format (rotation_by, push_index)
async def execute_action(action):
    color_index, push_index = action
    # [(2, 2), (2, 0), (3, 1), (2, 3), (1, 2), (2, 0), (3, 1), (2, 3)]
    # rotate_shaft(rotate_by)
    # push_cube(push_index)

    mag = [Magpositions.magA.value, Magpositions.magB.value, Magpositions.magC.value][
        color_index - 1
    ]
    plate = [
        Platepositions.plate1.value,
        Platepositions.plate2.value,
        Platepositions.plate3.value,
        Platepositions.plate4.value,
    ][push_index]

    await place_cube(mag, plate)
