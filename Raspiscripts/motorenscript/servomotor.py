import time

import RPi.GPIO as GPIO

# GPIO-Pin, an den der Servomotor angeschlossen ist
servoPin = 18  # Ersetzen Sie 18 durch Ihren GPIO-Pin

# GPIO-Modus einstellen
GPIO.setmode(GPIO.BCM)

# Pin als Ausgang festlegen
GPIO.setup(servoPin, GPIO.OUT)

# PWM-Instanz auf dem Servo-Pin mit 50Hz erstellen (üblich für Servomotoren)
pwm = GPIO.PWM(servoPin, 50)
pwm.start(0)


def set_servo_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servoPin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servoPin, False)
    pwm.ChangeDutyCycle(0)


try:
    # Den Servo zu verschiedenen Winkeln bewegen
    set_servo_angle(45)  # Bewegt den Servo auf 45 Grad
    set_servo_angle(90)  # Bewegt den Servo auf 90 Grad
    set_servo_angle(135)  # Bewegt den Servo auf 135 Grad

finally:
    # PWM stoppen und GPIO-Pins aufräumen
    pwm.stop()
    GPIO.cleanup()

print("Servo-Test abgeschlossen")
