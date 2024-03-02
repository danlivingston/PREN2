import time

import RPi.GPIO as GPIO

# GPIO-Pin-Definitionen
dirPin = 20  # Richtungspin
stepPin = 21  # Schrittpin
GPIO.setmode(GPIO.BCM)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(stepPin, GPIO.OUT)

# Anzahl der Schritte pro Umdrehung (abhängig von Ihrem Motor)
stepsPerRevolution = 200


# Motor drehen
def rotate_motor(steps, direction):
    GPIO.output(dirPin, direction)
    for i in range(steps):
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(stepPin, GPIO.LOW)
        time.sleep(0.01)


try:
    # Motor in eine Richtung drehen
    rotate_motor(stepsPerRevolution, True)
    time.sleep(2)

    # Motor in die andere Richtung drehen
    rotate_motor(stepsPerRevolution, False)

finally:
    GPIO.cleanup()

print("Schrittmotor-Test abgeschlossen")
