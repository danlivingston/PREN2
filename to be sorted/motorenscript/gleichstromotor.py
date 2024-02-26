import time

import RPi.GPIO as GPIO

# GPIO-Pin-Definitionen
motorPin1 = 23  # IN1 an der H-Brücke
motorPin2 = 24  # IN2 an der H-Brücke
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)


def motor_forward():
    GPIO.output(motorPin1, GPIO.HIGH)
    GPIO.output(motorPin2, GPIO.LOW)


def motor_backward():
    GPIO.output(motorPin1, GPIO.LOW)
    GPIO.output(motorPin2, GPIO.HIGH)


def motor_stop():
    GPIO.output(motorPin1, GPIO.LOW)
    GPIO.output(motorPin2, GPIO.LOW)


try:
    # Motor vorwärts
    motor_forward()
    time.sleep(5)

    # Motor anhalten
    motor_stop()
    time.sleep(2)

    # Motor rückwärts
    motor_backward()
    time.sleep(5)

    # Motor anhalten
    motor_stop()

finally:
    GPIO.cleanup()

print("Gleichstrommotor-Test abgeschlossen")
