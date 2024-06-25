import asyncio

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
buzzer = 26

GPIO.setup(buzzer, GPIO.OUT)


async def sound_beep(delay=0.1):
    GPIO.output(buzzer, 1)
    await asyncio.sleep(delay)
    GPIO.output(buzzer, 0)


async def sound_start():
    delay = 0.05
    await sound_beep(0.1)
    await asyncio.sleep(delay)
    await sound_beep(0.2)


async def sound_stop():
    delay = 0.05
    await sound_beep(0.1)
    await asyncio.sleep(delay)
    await sound_beep(0.1)
    await asyncio.sleep(delay)
    await sound_beep(0.1)


# TODO: error sound


async def sound_touch(freq):
    await sound_beep(0.1)
