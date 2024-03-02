import json
from datetime import datetime

import requests

# Basis URL
BASE_URL = "http://18.192.48.168:5000"  # Ändern Sie dies entsprechend

# Team spezifische URL und Auth-Token
TEAM_URL = f"{BASE_URL}/cubes/team12"
AUTH_TOKEN = "IhrAuthTokenHier"


# Funktion zum Lesen der Konfiguration aus einer JSON-Datei
def read_config_from_file(file_name):
    with open(file_name, "r") as file:
        return json.load(file)


# Lesen der Konfiguration aus der Datei "config01.json"
payload = read_config_from_file("config01.json")

# Fügen Sie das aktuelle Datum und Uhrzeit hinzu
payload["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

headers = {"Content-Type": "application/json", "Auth": AUTH_TOKEN}

# HTTP POST Anfrage
response = requests.post(TEAM_URL, headers=headers, data=json.dumps(payload))

# Überprüfung der Antwort
if response.status_code == 200:
    print("Daten erfolgreich gesendet.")
elif response.status_code == 204:
    print("Anfrage erfolgreich, aber keine weitere Information zurückgegeben.")
elif response.status_code == 405:
    print("Methode nicht erlaubt.")
elif response.status_code == 415:
    print("Media Type nicht unterstützt.")
elif response.status_code == 400:
    print("Bad Request.")
elif response.status_code == 500:
    print("Interner Serverfehler.")
else:
    print(f"Unerwarteter Statuscode: {response.status_code}")
