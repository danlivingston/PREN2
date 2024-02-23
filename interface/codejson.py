import json

# Pfad zur JSON-Datei
file_path = 'config01.json'

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
        
