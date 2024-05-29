import json
import os
from datetime import datetime

import requests


# Test Server Status
def test_server_reachability(url):
    get_url = f"{url}/cubes"

    try:
        # Anfrage mit einem Timeout von 8 Sekunden
        response = requests.get(get_url, timeout=5)
        if response.status_code == 200:
            print("Server ist erreichbar. Antwort:", response.text)
        else:
            print(
                f"Server möglicherweise nicht erreichbar. Statuscode {response.status_code}"
            )
    except requests.exceptions.Timeout:
        print("Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


# Start Signal
def send_start_signal(url, team_id, auth_token):
    headers = {"Content-Type": "application/json", "Auth": auth_token}
    post_url = f"{url}/cubes/{team_id}/start"

    try:
        response = requests.post(post_url, headers=headers, timeout=5)

        if response.status_code == 200:
            print(
                "200 OK: Request wurde akzeptiert. Informationen im Body der HTTP-Meldung vorhanden."
            )
        elif response.status_code == 204:
            print(
                "204 No Content: START Request wurde akzeptiert. Keine weiteren Daten im HTTP Body."
            )
        elif response.status_code == 405:
            print("405 Method Not Allowed: Der Request auf die URL war kein POST.")
        elif response.status_code == 401:
            print(
                "401 Unauthorized: Das Feld 'Auth' fehlt im Header des HTTP Request, der 'teamxx' Teil der URL entspricht keinem gültigen Team, oder das Token im Feld 'Auth' entspricht nicht dem Passwort des Teams xx."
            )
        elif response.status_code == 415:
            print(
                "415 Media Type Not Supported: Der Content Type ist nicht 'application/json'."
            )
        elif response.status_code == 400:
            print(
                "400 Bad Request: Der Body des Requests konnte nicht als json reparsed werden oder die übermittelten Daten entsprechen nicht dem Schema."
            )
        elif response.status_code == 500:
            print(
                "500 Internal Server Error: Fehler auf dem Applikations Server oder Versuch nicht existierende Daten in der DB zu lesen oder zu schreiben."
            )
        else:
            print(f"Unbekannter Statuscode {response.status_code}: {response.text}")

    except requests.exceptions.Timeout:
        print(
            "Die Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar oder Antwort verzögert."
        )
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)


def send_and_configure_cube(url, team_id, auth_token, config_data):
    try:
        # Aktualisieren der Zeit im config_data vor dem Senden
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        config_data["time"] = current_time

        headers = {"Content-Type": "application/json", "Auth": auth_token}
        post_url = f"{url}/cubes/{team_id}/config"

        # Senden des POST-Requests mit einem Timeout von 8 Sekunden
        response = requests.post(
            post_url, data=json.dumps(config_data), headers=headers, timeout=5
        )

        # Auswertung des Statuscodes und Ausgabe der entsprechenden Nachricht
        if response.status_code == 200:
            print(
                "200 OK: Request wurde akzeptiert. Informationen im Body HTTP Meldung vorhanden."
            )
        elif response.status_code == 204:
            print(
                "204 No Content: CONFIG Request wurde akzeptiert. Keine weiteren Daten im HTTP Body."
            )
        elif response.status_code == 405:
            print("405 Method Not Allowed: Der Request auf die URL war kein POST.")
        elif response.status_code == 401:
            print(
                "401 Unauthorized: Das Feld 'Auth' fehlt im Header des HTTP Request, der 'teamxx' Teil der URL entspricht keinem gültigen Team, oder das Token im Feld 'Auth' entspricht nicht dem Passwort des Teams xx."
            )
        elif response.status_code == 415:
            print(
                "415 Media Type Not Supported: Der Content Type ist nicht 'application/json'."
            )
        elif response.status_code == 400:
            print(
                "400 Bad Request: Der Body des Requests konnte nicht als json reparsed werden oder die übermittelten Daten entsprechen nicht dem Schema."
            )
        elif response.status_code == 500:
            print(
                "500 Internal Server Error: Fehler auf dem Applikations Server oder Versuch nicht existierende Daten in der DB zu lesen oder zu schreiben."
            )
        else:
            print(f"Unbekannter Statuscode {response.status_code}: {response.text}")

    except requests.exceptions.Timeout:
        print(
            "Die Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar oder Antwort verzögert."
        )
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)


# Beispielaufruf mit direkter Konfiguration
config_data = {
    "time": "",
    "config": {
        "1": "red",
        "2": "blue",
        "3": "red",
        "4": "red",
        "5": "blue",
        "6": "yellow",
        "7": "",
        "8": "",
    },
}


# End Signal
def send_end_signal(url, team_id, auth_token):
    headers = {"Content-Type": "application/json", "Auth": auth_token}
    post_url = f"{url}/cubes/{team_id}/end"

    try:
        response = requests.post(post_url, headers=headers, timeout=5)

        if response.status_code == 200:
            print(
                "200 OK: Request wurde akzeptiert. Informationen im Body der HTTP-Meldung vorhanden."
            )
        elif response.status_code == 204:
            print(
                "204 No Content: END Request wurde akzeptiert. Keine weiteren Daten im HTTP Body."
            )
        elif response.status_code == 405:
            print("405 Method Not Allowed: Der Request auf die URL war kein POST.")
        elif response.status_code == 401:
            print(
                "401 Unauthorized: Das Feld 'Auth' fehlt im Header des HTTP Request, der 'teamxx' Teil der URL entspricht keinem gültigen Team, oder das Token im Feld 'Auth' entspricht nicht dem Passwort des Teams xx."
            )
        elif response.status_code == 415:
            print(
                "415 Media Type Not Supported: Der Content Type ist nicht 'application/json'."
            )
        elif response.status_code == 400:
            print(
                "400 Bad Request: Der Body des Requests konnte nicht als json reparsed werden oder die übermittelten Daten entsprechen nicht dem Schema."
            )
        elif response.status_code == 500:
            print(
                "500 Internal Server Error: Fehler auf dem Applikations Server oder Versuch nicht existierende Daten in der DB zu lesen oder zu schreiben."
            )
        else:
            print(f"Unbekannter Statuscode {response.status_code}: {response.text}")

    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)


# Rückgabe Config und Zeit
def get_current_entries(url, team_id):
    get_url = f"{url}/cubes/{team_id}"

    try:
        response = requests.get(get_url, timeout=8)
        if response.status_code == 200:
            print("Aktuelle Einträge erfolgreich abgerufen:")
            print(response.json())  # Anzeige der JSON-Antwort
        else:
            print(
                f"Fehler beim Abrufen der aktuellen Einträge: Statuscode {response.status_code}"
            )
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


# Beispielaufrufe
test_server_reachability("https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com")
send_start_signal(
    "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com",
    "team12",
    "R5SfQQ6gKr9A",
)
send_and_configure_cube(
    "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com",
    "team12",
    "R5SfQQ6gKr9A",
    config_data,
)
send_end_signal(
    "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com",
    "team12",
    "R5SfQQ6gKr9A",
)
get_current_entries(
    "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com", "team12"
)
