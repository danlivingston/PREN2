import requests

def test_server_reachability(url):
    get_url = f"{url}/cubes"
    
    try:
        # Anfrage mit einem Timeout von 5 Sekunden
        response = requests.get(get_url, timeout=6)
        if response.status_code == 200:
            print("Server ist erreichbar. Antwort:", response.text)
        else:
            print(f"Server möglicherweise nicht erreichbar. Statuscode {response.status_code}")
    except requests.exceptions.Timeout:
        # Spezifische Behandlung für einen Timeout-Fehler
        print("Anfrage hat zu lange gedauert. Server möglicherweise nicht erreichbar.")
    except Exception as e:
        # Allgemeine Fehlerbehandlung
        print(f"Ein Fehler ist aufgetreten: {e}")

test_server_reachability('http://52.58.217.104:5000')
