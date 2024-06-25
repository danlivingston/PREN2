import json
import os
from datetime import datetime

import requests
from loguru import logger

URL = os.getenv("API_URL", "")
TEAM_ID = os.getenv("TEAM_ID", "")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")


def get_log_message(response):
    match response.status_code:
        case 200:
            return "200 OK: Request wurde akzeptiert. Informationen im Body HTTP Meldung vorhanden."
        case 204:
            return "204 No Content: Request wurde akzeptiert. Keine weiteren Daten im HTTP Body."
        case 405:
            return "405 Method Not Allowed: Der Request auf die URL war kein POST."
        case 401:
            return (
                "401 Unauthorized: Das Feld 'Auth' fehlt im Header des HTTP Request, der 'teamxx' Teil der URL "
                "entspricht keinem gültigen Team, oder das Token im Feld 'Auth' entspricht nicht dem Passwort "
                "des Teams xx."
            )
        case 415:
            return "415 Media Type Not Supported: Der Content Type ist nicht 'application/json'."
        case 400:
            return (
                "400 Bad Request: Der Body des Requests konnte nicht als json reparsed werden oder die übermittelten "
                "Daten entsprechen nicht dem Schema."
            )
        case 500:
            return (
                "500 Internal Server Error: Fehler auf dem Applikations Server oder Versuch nicht existierende Daten "
                "in der DB zu lesen oder zu schreiben."
            )
        case _:
            return f"Unbekannter Statuscode {response.status_code}: {response.text}"


async def send_start_signal():
    logger.trace("sending start signal")
    headers = {"Content-Type": "application/json", "Auth": AUTH_TOKEN}
    post_url = f"{URL}/cubes/{TEAM_ID}/start"

    try:
        response = requests.post(post_url, headers=headers, timeout=15)
        logger.trace("sent start signal")
        logger.debug(get_log_message(response))
    except requests.exceptions.Timeout:
        logger.debug(
            "Die Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar oder Antwort verzögert."
        )
    except Exception as e:
        logger.exception(e)


async def send_end_signal():
    logger.trace("sending end signal")
    headers = {"Content-Type": "application/json", "Auth": AUTH_TOKEN}
    post_url = f"{URL}/cubes/{TEAM_ID}/end"

    try:
        response = requests.post(post_url, headers=headers, timeout=15)
        logger.trace("sent end signal")
        logger.debug(get_log_message(response))
    except requests.exceptions.Timeout:
        logger.debug(
            "Die Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar oder Antwort verzögert."
        )
    except Exception as e:
        logger.exception(e)


async def send_cube_configuration(config_data):
    # Aktualisieren der Zeit im config_data vor dem Senden
    config_data = json.loads(config_data)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config_data["time"] = current_time

    headers = {"Content-Type": "application/json", "Auth": AUTH_TOKEN}
    post_url = f"{URL}/cubes/{TEAM_ID}/config"

    try:
        response = requests.post(
            post_url, data=json.dumps(config_data), headers=headers, timeout=15
        )
        logger.debug(get_log_message(response))
    except requests.exceptions.Timeout:
        logger.debug(
            "Die Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar oder Antwort verzögert."
        )
    except Exception as e:
        logger.exception(e)


async def test_server_reachability():
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


async def get_current_entries():
    get_url = f"{URL}/cubes/{TEAM_ID}"

    try:
        response = requests.get(get_url, timeout=8)
        if response.status_code == 200:
            logger.trace(response.json())
            return response.json()
        else:
            raise Exception(
                f"Fehler beim Abrufen der aktuellen Einträge: Statuscode {response.status_code}"
            )
    except Exception as e:
        logger.exception(e)
        raise e
