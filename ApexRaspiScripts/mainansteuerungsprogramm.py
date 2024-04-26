import smbus2
import tkinter as tk
import threading 
import time
import os
from datetime import datetime
import RPi.GPIO as GPIO
import measurelib
from DRV8825 import DRV8825
from multiprocessing import Process
from enum import Enum

# Initialisierung des Schrittmotors
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor1.SetMicroStep('hardward' ,'1/4step')
Motor1.Stop()


endschalter=8
GPIO.setup(endschalter,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
channelX=10
GPIO.setup(channelX,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

sole1=14
sole2=23
sole3=5
sole4=6

GPIO.setup(sole1,GPIO.OUT)
GPIO.setup(sole2,GPIO.OUT)
GPIO.setup(sole3,GPIO.OUT)
GPIO.setup(sole4,GPIO.OUT)

masterposition = 0

class Magpositions(Enum):
	magA = 0
	magB = 1066
	magC = 2133
	
class Platepositions(Enum):
	plate1 = 0
	plate2 = 800
	plate3 = 1600
	plate4 = 2400

#magazin motor
def zero_mag():
	global masterposition
	while(GPIO.input(channelX)==0):
		Motor1.TurnStep(Dir='forward', steps=1, stepdelay=0.00005)
	Motor1.TurnStep(Dir='forward', steps=250, stepdelay=0.00005)
	time.sleep(0.2)
	Motor1.Stop()
	masterposition=0
	return()
	
def place_cube(mag, pos):
	global masterposition
	
	actualpos = masterposition + mag
	if actualpos >= 3200:
		actualpos -= 3200

	
	schritte= pos - actualpos
	if schritte < 0 :
		schritte = 3200 - abs(schritte)
	

	Motor1.TurnStep(Dir='forward', steps=schritte, stepdelay=0.00005)
	
	
	if pos == 0:
		GPIO.output(sole1,1)
		time.sleep(0.1)
		GPIO.output(sole1,0)
	elif pos == 800:
		GPIO.output(sole2,1)
		time.sleep(0.1)
		GPIO.output(sole2,0)
	elif pos == 1600:
		GPIO.output(sole3,1)
		time.sleep(0.1)
		GPIO.output(sole3,0)
	elif pos == 2400:
		GPIO.output(sole4,1)
		time.sleep(0.1)
		GPIO.output(sole4,0)
	
	time.sleep(0.1)
	masterposition += schritte
	if masterposition >= 3200:
		masterposition -= 3200
	return()
	

# Initialisierung der Stössel
r1 = PiRelay6.Relay("RELAY1")
r4 = PiRelay6.Relay("RELAY2")
r3 = PiRelay6.Relay("RELAY3")
r2 = PiRelay6.Relay("RELAY4")

def schrittmotorDrehen(grad):
    if grad == 0 or grad == 360:
        print("\tKeine Drehung erforderlich. Schrittmotor bleibt in Position.")
        return  # Frühe Rückkehr, um die Funktion zu beenden
    
    modifizierterGrad = 360 - grad
    schritteProUmdrehung = 800  
    modifizierterGrad = modifizierterGrad % 360  
    schritte = int((modifizierterGrad / 360.0) * schritteProUmdrehung)  # Schritte berechnen

    if grad != 0:
        print(f"\tSchrittmotor beginnt zu drehen um {modifizierterGrad} Grad vorwärts...")
        Motor1.TurnStep(Dir='forward', steps=schritte, stepdelay=0.0005)
        Motor1.Stop()
        time.sleep(0.1)  # Kurze Pause nach der Drehung
        print(f"\tSchrittmotor hat die Drehung abgeschlossen. ({schritte} Schritte)")
    else:
        print("\tKeine Drehung erforderlich. Schrittmotor bleibt in Position.")

def aktualisiereWuerfelPositionen(nachDrehung, farbenZuPosition):
    return {color: (position + nachDrehung) % 360 for color, position in farbenZuPosition.items()}

def berechneMagazinDrehungZuRelais(farbenZuPosition, zielFarbe, aktuelleMagazinPosition, zielRelais):
    relaisZuGrad = {1: 0, 2: 270, 3: 180, 4: 90}
    zielPosition = farbenZuPosition[zielFarbe]
    relaisPosition = relaisZuGrad[zielRelais]
    drehung = (relaisPosition - zielPosition + 360) % 360
    neueFarbenZuPosition = aktualisiereWuerfelPositionen(drehung, farbenZuPosition)
    return drehung, neueFarbenZuPosition

def relaisAktivieren(zielRelais):
    delay_hinten = 0.1
    delay_vorne = 0.2

    print(f"\tRelais {zielRelais} wird aktiviert, um den Würfel auszustoßen...")
    if zielRelais == 1:
        r1.on()
        time.sleep(delay_hinten)
        r1.off()
        time.sleep(delay_vorne)
    elif zielRelais == 2:
        r2.on()
        time.sleep(delay_hinten)
        r2.off()
        time.sleep(delay_vorne)
    elif zielRelais == 3:
        r3.on()
        time.sleep(delay_hinten)
        r3.off()
        time.sleep(delay_vorne)
    elif zielRelais == 4:
        r4.on()
        time.sleep(delay_hinten)
        r4.off()
        time.sleep(delay_vorne)
    print("\tWürfel wurde ausgestoßen.")

def sortiereWuerfel(konfiguration):
    try:
        startZeit = time.time()
        farbenZuPosition = {'blue': 0, 'red': 120, 'yellow': 240}
        print("Beginne Sortiervorgang...\n")
        for position, color in sorted(konfiguration.items(), key=lambda x: int(x[0])):
            if color:
                zielRelais = ((int(position) - 1) % 4) + 1
                print(f"Position {position}, Farbe '{color}':")
                drehung, neueFarbenZuPosition = berechneMagazinDrehungZuRelais(farbenZuPosition, color, position, zielRelais)
                schrittmotorDrehen(drehung)
                farbenZuPosition = neueFarbenZuPosition
                relaisAktivieren(zielRelais)
            else:
                print(f"Position {position} hat keinen Würfel. Überspringen...")
        endZeit = time.time()
        gesamtzeit = endZeit - startZeit
        print("\nSortierung abgeschlossen. Alle Würfel sind entsprechend der Konfiguration sortiert.")
        print(f"Gesamtzeit für den Sortiervorgang: {gesamtzeit:.2f} Sekunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        GPIO.cleanup()
        Motor1.Stop()
        print("Aufräumarbeiten abgeschlossen.")

# Testkonfiguration
konfiguration = {
    "1": "blue",  
    "2": "yellow",   
    "3": "",
    "4": "blue", 
    "5": "red",  
    "6": "red",
    "7": "blue",
    "8": "yellow"  
}

sortiereWuerfel(konfiguration)
