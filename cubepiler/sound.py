import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
buzzer = 11

GPIO.setup(buzzer, GPIO.OUT)


def sound_start(freq):
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


def sound_stop(freq):
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


# sound_start(600)
# time.sleep(1)
# sound_stop(600)


def sound_cleanup():
    GPIO.cleanup()
