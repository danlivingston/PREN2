import requests
import json
from datetime import datetime
import os

def send_cube_configuration(url, team_id, auth_token, config_data):
    # Aktualisieren der Zeit im config_data vor dem Senden
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config_data["time"] = current_time
    
    headers = {'Content-Type': 'application/json', 'Auth': auth_token}
    post_url = f"{url}/cubes/{team_id}/config"
    
    try:
        response = requests.post(post_url, data=json.dumps(config_data), headers=headers)
        # Auswertung des Statuscodes und Ausgabe der entsprechenden Nachricht
        if response.status_code == 200:
            print("200 OK: Request wurde akzeptiert. Informationen im Body HTTP Meldung vorhanden.")
        elif response.status_code == 204:
            print("204 No Content: Request wurde akzeptiert. Keine weiteren Daten im HTTP Body.")
        elif response.status_code == 405:
            print("405 Method Not Allowed: Der Request auf die URL war kein POST.")
        elif response.status_code == 401:
            print("401 Unauthorized: Das Feld 'Auth' fehlt im Header des HTTP Request, der 'teamxx' Teil der URL entspricht keinem gültigen Team, oder das Token im Feld 'Auth' entspricht nicht dem Passwort des Teams xx.")
        elif response.status_code == 415:
            print("415 Media Type Not Supported: Der Content Type ist nicht 'application/json'.")
        elif response.status_code == 400:
            print("400 Bad Request: Der Body des Requests konnte nicht als json reparsed werden oder die übermittelten Daten entsprechen nicht dem Schema.")
        elif response.status_code == 500:
            print("500 Internal Server Error: Fehler auf dem Applikations Server oder Versuch nicht existierende Daten in der DB zu lesen oder zu schreiben.")
        else:
            print(f"Unbekannter Statuscode {response.status_code}: {response.text}")
            
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)
        
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file_path = os.path.join(base_dir, 'config.json')

try:
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)
except FileNotFoundError:
    print("Die Konfigurationsdatei konnte nicht gefunden werden.")
except json.JSONDecodeError:
    print("Die Konfigurationsdatei konnte nicht korrekt geparst werden.")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
else:
    # Beispielaufruf der Funktion mit den gelesenen Konfigurationsdaten
    send_cube_configuration('http://52.58.217.104:5000', 'team12', 'R5SfQQ6gKr9A', config_data)

#send_cube_configuration('http://52.58.217.104:5000', 'team00', 'aTdpCRIrI9CLS1', config_data)