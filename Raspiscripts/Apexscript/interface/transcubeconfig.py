import requests
import json

def send_cube_configuration(url, team_id, auth_token, config_data):
    headers = {'Content-Type': 'application/json', 'Auth': auth_token}
    post_url = f"{url}/cubes/{team_id}/config"
    response = requests.post(post_url, data=json.dumps(config_data), headers=headers)
    print(response.text)

# Beispielkonfiguration
config_data = {
    "time": "2024-03-14 15:10:05",
    "config": {
        "1": "red",
        "2": "blue",
        "3": "red",
        "4": "yellow",
        "5": "",
        "6": "",
        "7": "yellow",
        "8": "red"
    }
}

#'IhrTokenHier' durch Ihr tatsächliches Authentifizierungstoken ersetzen:)
send_cube_configuration('http://52.58.217.104:5000', 'team12', 'IhrTokenHier', config_data)
