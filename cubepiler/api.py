import json
from datetime import datetime

import requests
from loguru import logger

import os

URL = os.getenv("URL", "")
TEAM_ID = os.getenv("TEAM_ID", "")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")


def send_start_signal():
    headers = {"Content-Type": "application/json", "Auth": AUTH_TOKEN}
    post_url = f"{URL}/cubes/{TEAM_ID}/start"

    try:
        # POST-Anfrage mit einem Timeout von 5 Sekunden
        response = requests.post(post_url, headers=headers, timeout=8)

        # Auswertung des Statuscodes und Ausgabe der entsprechenden Nachricht
        if response.status_code == 200:
            logger.debug(
                "200 OK: Request wurde akzeptiert. Informationen im Body der HTTP-Meldung vorhanden."
            )
        elif response.status_code == 204:
            logger.debug(
                "204 No Content: Request wurde akzeptiert. Keine weiteren Daten im HTTP Body."
            )
        elif response.status_code == 405:
            logger.debug(
                "405 Method Not Allowed: Der Request auf die URL war kein POST."
            )
        elif response.status_code == 401:
            logger.debug(
                "401 Unauthorized: Das Feld 'Auth' fehlt im Header des HTTP Request, der 'teamxx' Teil der URL entspricht keinem gültigen Team, oder das Token im Feld 'Auth' entspricht nicht dem Passwort des Teams xx."
            )
        elif response.status_code == 415:
            logger.debug(
                "415 Media Type Not Supported: Der Content Type ist nicht 'application/json'."
            )
        elif response.status_code == 400:
            logger.debug(
                "400 Bad Request: Der Body des Requests konnte nicht als json reparsed werden oder die übermittelten Daten entsprechen nicht dem Schema."
            )
        elif response.status_code == 500:
            logger.debug(
                "500 Internal Server Error: Fehler auf dem Applikations Server oder Versuch nicht existierende Daten in der DB zu lesen oder zu schreiben."
            )
        else:
            logger.debug(
                f"Unbekannter Statuscode {response.status_code}: {response.text}"
            )

    except requests.exceptions.Timeout:
        # Spezifische Behandlung für einen Timeout-Fehler
        logger.debug(
            "Die Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar oder Antwort verzögert."
        )
    except Exception as e:
        # Allgemeine Fehlerbehandlung
        logger.debug("Ein Fehler ist aufgetreten:", e)


def send_end_signal():
    headers = {"Content-Type": "application/json", "Auth": AUTH_TOKEN}
    post_url = f"{URL}/cubes/{TEAM_ID}/end"

    try:
        response = requests.post(post_url, headers=headers, timeout=8)

        # Auswertung des Statuscodes und Ausgabe der entsprechenden Nachricht
        if response.status_code == 200:
            logger.debug(
                "200 OK: Request wurde akzeptiert. Informationen im Body der HTTP-Meldung vorhanden."
            )
        elif response.status_code == 204:
            logger.debug(
                "204 No Content: Request wurde akzeptiert. Keine weiteren Daten im HTTP Body."
            )
        elif response.status_code == 405:
            logger.debug(
                "405 Method Not Allowed: Der Request auf die URL war kein POST."
            )
        elif response.status_code == 401:
            logger.debug(
                "401 Unauthorized: Das Feld 'Auth' fehlt im Header des HTTP Request, der 'teamxx' Teil der URL entspricht keinem gültigen Team, oder das Token im Feld 'Auth' entspricht nicht dem Passwort des Teams xx."
            )
        elif response.status_code == 415:
            logger.debug(
                "415 Media Type Not Supported: Der Content Type ist nicht 'application/json'."
            )
        elif response.status_code == 400:
            logger.debug(
                "400 Bad Request: Der Body des Requests konnte nicht als json reparsed werden oder die übermittelten Daten entsprechen nicht dem Schema."
            )
        elif response.status_code == 500:
            logger.debug(
                "500 Internal Server Error: Fehler auf dem Applikations Server oder Versuch nicht existierende Daten in der DB zu lesen oder zu schreiben."
            )
        else:
            logger.debug(
                f"Unbekannter Statuscode {response.status_code}: {response.text}"
            )

    except Exception as e:
        logger.debug("Ein Fehler ist aufgetreten:", e)


def send_cube_configuration(config_data):
    # Aktualisieren der Zeit im config_data vor dem Senden
    config_data = json.loads(config_data)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config_data["time"] = current_time

    headers = {"Content-Type": "application/json", "Auth": AUTH_TOKEN}
    post_url = f"{URL}/cubes/{TEAM_ID}/config"

    try:
        # Senden des POST-Requests mit einem Timeout von 5 Sekunden
        response = requests.post(
            post_url, data=json.dumps(config_data), headers=headers, timeout=8
        )

        # Auswertung des Statuscodes und Ausgabe der entsprechenden Nachricht
        if response.status_code == 200:
            logger.debug(
                "200 OK: Request wurde akzeptiert. Informationen im Body HTTP Meldung vorhanden."
            )
        elif response.status_code == 204:
            logger.debug(
                "204 No Content: Request wurde akzeptiert. Keine weiteren Daten im HTTP Body."
            )
        elif response.status_code == 405:
            logger.debug(
                "405 Method Not Allowed: Der Request auf die URL war kein POST."
            )
        elif response.status_code == 401:
            logger.debug(
                "401 Unauthorized: Das Feld 'Auth' fehlt im Header des HTTP Request, der 'teamxx' Teil der URL entspricht keinem gültigen Team, oder das Token im Feld 'Auth' entspricht nicht dem Passwort des Teams xx."
            )
        elif response.status_code == 415:
            logger.debug(
                "415 Media Type Not Supported: Der Content Type ist nicht 'application/json'."
            )
        elif response.status_code == 400:
            logger.debug(
                "400 Bad Request: Der Body des Requests konnte nicht als json reparsed werden oder die übermittelten Daten entsprechen nicht dem Schema."
            )
        elif response.status_code == 500:
            logger.debug(
                "500 Internal Server Error: Fehler auf dem Applikations Server oder Versuch nicht existierende Daten in der DB zu lesen oder zu schreiben."
            )
        else:
            logger.debug(
                f"Unbekannter Statuscode {response.status_code}: {response.text}"
            )

    except requests.exceptions.Timeout:
        logger.debug(
            "Die Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar oder Antwort verzögert."
        )
    except Exception as e:
        logger.debug("Ein Fehler ist aufgetreten:", e)


# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# config_file_path = os.path.join(base_dir, "config.json")

# try:
#     with open(config_file_path, "r") as file:
#         config_data = json.load(file)
# except FileNotFoundError:
#     logger.debug("Die Konfigurationsdatei konnte nicht gefunden werden.")
# except json.JSONDecodeError:
#     logger.debug("Die Konfigurationsdatei konnte nicht korrekt geparst werden.")
# except Exception as e:
#     logger.debug(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
# else:
#     # Beispielaufruf der Funktion mit den gelesenen Konfigurationsdaten
#     send_cube_configuration(
#         "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com",
#         "team12",
#         "R5SfQQ6gKr9A",
#         config_data,
#     )


def test_server_reachability():
    get_url = f"{URL}/cubes"

    try:
        # Anfrage mit einem Timeout von 5 Sekunden
        response = requests.get(get_url, timeout=8)
        if response.status_code == 200:
            logger.debug("Server ist erreichbar. Antwort:", response.text)
        else:
            logger.debug(
                f"Server möglicherweise nicht erreichbar. Statuscode {response.status_code}"
            )
    except requests.exceptions.Timeout:
        # Spezifische Behandlung für einen Timeout-Fehler
        logger.debug(
            "Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar."
        )
    except Exception as e:
        # Allgemeine Fehlerbehandlung
        logger.debug(f"Ein Fehler ist aufgetreten: {e}")


# test_server_reachability("https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com")


def get_current_entries():
    get_url = f"{URL}/cubes/{TEAM_ID}"

    try:
        response = requests.get(get_url, timeout=8)
        if response.status_code == 200:
            logger.debug("Aktuelle Einträge erfolgreich abgerufen:")
            logger.debug(response.json())
        else:
            logger.debug(
                f"Fehler beim Abrufen der aktuellen Einträge: Statuscode {response.status_code}"
            )
    except Exception as e:
        logger.debug(f"Ein Fehler ist aufgetreten: {e}")


# get_current_entries(
#     "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com", "team12"
# )
