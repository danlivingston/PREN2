import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
buzzer = 26

GPIO.setup(buzzer, GPIO.OUT)


async def sound_start(freq=300):
    i = 0
    delay = 0.5 / freq
    while i < 70:
        GPIO.output(buzzer, 1)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += 1
    delay = delay / 10
    i = 0
    while i < 300:
        GPIO.output(buzzer, 1)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += 1


async def sound_stop(freq=500):
    i = 0
    delay = 0.05 / freq
    while i < 300:
        GPIO.output(buzzer, 1)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += 1
    delay = 0.5 / freq
    i = 0
    while i < 70:
        GPIO.output(buzzer, 1)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += 1


async def sound_touch(freq):
    i = 0
    frequency = freq
    delay = 1 / (2 * frequency)
    while i < 300:
        GPIO.output(buzzer, 1)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += 1


"""

sound_start(600)
time.sleep(1)
sound_stop(600)
time.sleep(1)
sound_touch(10000)

GPIO.cleanup()
"""
