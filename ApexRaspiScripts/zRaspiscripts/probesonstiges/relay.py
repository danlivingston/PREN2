#!/usr/bin/python3
import time
import RPi.GPIO as GPIO
import json
import os
import sys

#Haltemagazin
# 1. Position Blau 
# 2. Position Rot 
# 3. Position gelb
# 4. Position Leer

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

# Funktion zum Lesen der JSON-Konfiguration
def read_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
    
def rotate_step_motor(steps, direction):
    # Hier müsst ihr euren Code für die Ansteuerung des Schrittmotors hinzufügen
    # Zum Beispiel:
    # for _ in range(steps):
    #     # Schrittmotor ein Schritt vorwärts oder rückwärts
    #     time.sleep(0.01)  # Pausieren für X Sekunden
    pass

# Beispiel zur Verwendung des Relais
r3.on()
time.sleep(0.5)
r3.off()

def main():
    # Basisverzeichnis relativ zum aktuellen Skript ermitteln
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Pfad zur JSON-Datei, direkt im Basisverzeichnis
    file_path = os.path.join(base_dir, 'config.json')

    # JSON-Datei öffnen und einlesen
    config = read_config(file_path)
    
    for position, desired_color in config["config"].items():
        if desired_color:  # Falls eine Farbe zugewiesen ist
            # Entsprechendes Relais für die Farbe finden
            for relay_name, relay in relays.items():
                if desired_color == "blue" and relay_name == "Relay 1":
                    relay.on()
                    time.sleep(0.5)  # Pausieren, um den Würfel vollständig auszustoßen
                    relay.off()
                elif desired_color == "red" and relay_name == "Relay 2":
                    relay.on()
                    time.sleep(0.5)
                    relay.off()
                elif desired_color == "yellow" and relay_name == "Relay 3":
                    relay.on()
                    time.sleep(0.5)
                    relay.off()
                # Fügen Sie hier Bedingungen für weitere Farben hinzu, falls nötig
        else:
            print(f"Position {position} hat keine zugewiesene Farbe.")

if __name__ == '__main__':
    main()