import os
import platform
import subprocess
import time

def get_cpu_temperature_mac():
    try:
        # Nutze 'osx-cpu-temp', um die CPU-Temperatur auf einem Mac zu lesen
        temp = subprocess.check_output(['osx-cpu-temp']).decode('utf-8').strip()
        print(f"MacBook CPU Temperatur: {temp}")
    except Exception as e:
        print(f"Fehler beim Auslesen der CPU-Temperatur auf dem MacBook: {e}")

def get_cpu_temperature_raspi():
    try:
        # Lies die CPU-Temperatur direkt aus dem Systemverzeichnis auf dem Raspberry Pi
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read()) / 1000
        print(f"Raspberry Pi CPU Temperatur: {temp}°C")
    except Exception as e:
        print(f"Fehler beim Auslesen der CPU-Temperatur auf dem Raspberry Pi: {e}")

def main():
    try:
        while True:
            if platform.system() == 'Darwin':
                get_cpu_temperature_mac()
            elif platform.system() == 'Linux':
                get_cpu_temperature_raspi()
            else:
                print("Unbekannte Plattform. Dieses Skript unterstützt nur macOS und Raspberry Pi Linux.")
            time.sleep(1)  # Warte eine Sekunde bevor die nächste Messung durchgeführt wird.
    except KeyboardInterrupt:
        print("Skript wurde durch Benutzereingriff beendet.")

main()
