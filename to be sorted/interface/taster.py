import subprocess
import time

import RPi.GPIO as GPIO

# Konfigurieren Sie den GPIO-Pin
# GPIO17 = 11 und bei Pin 1
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def run_json_script():
    # Pfad zum Skript, das ausgeführt werden soll
    script_path = "codejsontaster.py"

    # Starten Sie das Skript mit Python3
    subprocess.run(["python3", script_path])


# Warte auf Tastendruck
try:
    print("Bereit für Tastendruck...")
    while True:
        # Überprüfen, ob der Taster gedrückt ist
        if GPIO.input(button_pin) == GPIO.HIGH:
            run_json_script()
            # Entprellzeit
            time.sleep(0.5)
except KeyboardInterrupt:
    # Bereinige die Konfiguration bei Programmende
    GPIO.cleanup()
    print("Programm durch Benutzer gestoppt.")
