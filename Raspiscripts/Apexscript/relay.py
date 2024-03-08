#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

# Initialisieren von GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Relay:
    """Klasse zur Steuerung eines Relais"""
    relaypins = {
        "RELAY1": 29,
        "RELAY2": 31,
        "RELAY3": 33,
        "RELAY4": 35,
        "RELAY5": 37,
        "RELAY6": 40,
    }

    def __init__(self, relay):
        self.pin = self.relaypins[relay]
        self.relay = relay
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        print(self.relay + " - ON")
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        print(self.relay + " - OFF")
        GPIO.output(self.pin, GPIO.LOW)

# Erstellen von Relay-Instanzen
r1 = Relay("RELAY1")
r2 = Relay("RELAY2")
r3 = Relay("RELAY3")
r4 = Relay("RELAY4")
r5 = Relay("RELAY5")
r6 = Relay("RELAY6")

# Beispiel zur Verwendung des Relais
r3.on()
time.sleep(0.5)
r3.off()
