#!/usr/bin/python3

# Library for PiRelay 6 
# Developed by: SB Components
# Author: Satyam
# Project: PiRelay6-Channel
# Python: 3.7.3


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Relay:
    ''' Class to handle Relay
    Arguments:
    relay = string Relay label (i.e. "RELAY1","RELAY2","RELAY3","RELAY4","RELAY5","RELAY6")
    '''
    relaypins = {"RELAY1":14, "RELAY2":23, "RELAY3":5, "RELAY4":6, "RELAY5":2, "RELAY6":2}


    def __init__(self, relay):
        self.pin = self.relaypins[relay]
        self.relay = relay
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        print(self.relay + " - ON")
        GPIO.output(self.pin,GPIO.HIGH)

    def off(self):
        print(self.relay + " - OFF")
        GPIO.output(self.pin,GPIO.LOW)
