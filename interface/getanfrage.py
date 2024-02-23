import requests
import pygame
import time

# Initialisierung von Pygame für die Tonausgabe
pygame.init()
pygame.mixer.init()

# URL des Servers
url = "http://18.192.48.168:5000/cubes"

# Durchführung der GET-Anfrage
response = requests.get(url)

# Überprüfung des Status-Codes der Antwort
if response.status_code == 200:
    print("Server erreichbar. Antwort:", response.text)
else:
    print(f"Fehler: Erhielt Status-Code {response.status_code}")
