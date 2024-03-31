import time

import RPi.GPIO as GPIO

# GPIO-Pin, an den der Servomotor angeschlossen ist (z.B. GPIO 17)
servoPin = 17

# GPIO-Modus einstellen
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

# PWM-Instanz auf dem Servo-Pin mit 50Hz erstellen (üblich für Servomotoren)
pwm = GPIO.PWM(servoPin, 50)
pwm.start(0)


def set_servo_angle(angle):
    duty_cycle = (angle / 18) + 2
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)


try:
    # Den Servomotor auf verschiedene Winkel setzen
    set_servo_angle(45)  # Bewegt den Servo auf 45 Grad
    set_servo_angle(90)  # Bewegt den Servo auf 90 Grad
    set_servo_angle(135)  # Bewegt den Servo auf 135 Grad

finally:
    # PWM stoppen und GPIO-Pins aufräumen
    pwm.stop()
    GPIO.cleanup()

print("Servomotor-Test abgeschlossen")
