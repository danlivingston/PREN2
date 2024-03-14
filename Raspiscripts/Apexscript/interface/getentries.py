import requests

def get_current_entries(url, team_id):
    get_url = f"{url}/cubes/{team_id}"
    
    try:
        response = requests.get(get_url)
        if response.status_code == 200:
            print("Aktuelle Einträge erfolgreich abgerufen:")
            print(response.json()) 
        else:
            print(f"Fehler beim Abrufen der aktuellen Einträge: Statuscode {response.status_code}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


get_current_entries('http://52.58.217.104:5000', 'team12')