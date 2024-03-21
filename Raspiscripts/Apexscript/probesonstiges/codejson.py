import json
import sys
import os

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Pfad zur JSON-Datei, relativ zum Basisverzeichnis
file_path = os.path.join(base_dir, 'videos', 'config01.json')

# JSON-Datei öffnen und einlesen
with open(file_path, 'r') as file:
    data = json.load(file)

# Durch die Konfigurationseinträge gehen
for key, value in data['config'].items():
    if value == "yellow":
        print(f"Key {key}: Ausführen des Befehls für Gelb")
    elif value == "red":
        print(f"Key {key}: Ausführen des Befehls für Rot")
    elif value == "blue":
        print(f"Key {key}: Ausführen des Befehls für Blau")
    else:
        print(f"Key {key}: Kein Befehl definiert")

# Skript explizit beenden
sys.exit()
