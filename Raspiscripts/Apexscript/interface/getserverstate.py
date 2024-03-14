import requests

def test_server_reachability(url):
    get_url = f"{url}/cubes"
    
    try:
        response = requests.get(get_url)
        if response.status_code == 200:
            print("Server ist erreichbar. Antwort:", response.text)
        else:
            print(f"Server möglicherweise nicht erreichbar. Statuscode {response.status_code}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


test_server_reachability('http://52.58.217.104:5000')
