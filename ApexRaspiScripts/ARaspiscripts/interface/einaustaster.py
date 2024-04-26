import RPi.GPIO as GPIO
import time
import subprocess

# Konfigurieren Sie die GPIO-Pins für die Taster
button_pin1 = 17  # Erster Taster
button_pin2 = 18  # Zweiter Taster
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def run_script1():
    # Pfad zum ersten Skript, das ausgeführt werden soll
    script_path = 'script1.py'
    
    # Starten Sie das Skript mit Python3
    subprocess.run(['python3', script_path])

def run_script2():
    # Pfad zum zweiten Skript, das ausgeführt werden soll
    script_path = 'script2.py'
    
    # Starten Sie das Skript mit Python3
    subprocess.run(['python3', script_path])

# Warte auf Tastendruck
try:
    print("Bereit für Tastendruck...")
    while True:
        # Überprüfen, ob der erste Taster gedrückt ist
        if GPIO.input(button_pin1) == GPIO.HIGH:
            run_script1()
            # Entprellzeit
            time.sleep(0.5)
        
        # Überprüfen, ob der zweite Taster gedrückt ist
        if GPIO.input(button_pin2) == GPIO.HIGH:
            run_script2()
            # Entprellzeit
            time.sleep(0.5)
except KeyboardInterrupt:
    # Bereinige die Konfiguration bei Programmende
    GPIO.cleanup()
    print("Programm durch Benutzer gestoppt.")
