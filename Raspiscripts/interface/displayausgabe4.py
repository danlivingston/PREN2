import random
import json
import time
import pygame

# Basisverzeichnis relativ zum aktuellen Skript ermitteln
base_dir = os.path.dirname(os.path.abspath(__file__))

# Pfad zur JSON-Datei im "videos"-Ordner
json_file_path = os.path.join(base_dir, 'config03.json')

# JSON-Daten einlesen
with open(json_file_path, 'r') as file:
    data = json.load(file)
config = data['config']

# Bildschirmgröße
screen_width = 800
screen_height = 600

# Anzahl der Würfel
num_dice = 8

# Größe der Würfel
dice_size = 100

# Abstand zwischen den Würfeln
dice_spacing = 20

# Farben aus JSON-Datei
colors = config['colors']

# Initialisierung von Pygame
pygame.init()

# Fenster erstellen
screen = pygame.display.set_mode((screen_width, screen_height))

# Position des Fensters auf der rechten Bildschirmseite
screen.set_position((screen_width - screen_width // 2, 0))

# Hintergrundfarbe
screen.fill((255, 255, 255))

# Liste der Würfel-Objekte
dice = []

# Erstellen der Würfel-Objekte
for i in range(num_dice):
    # Zufällige Farbe aus der Liste wählen
    color = random.choice(colors)

    # Position des Würfels berechnen
    x = i * (dice_size + dice_spacing) + dice_spacing
    y = dice_spacing

    # Würfel-Objekt erstellen
    dice.append(pygame.Rect(x, y, dice_size, dice_size))

# Spielschleife
while True:
    # Ereignisse abhandeln
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Bildschirm füllen
    screen.fill((255, 255, 255))

    # Würfel zeichnen
    for die in dice:
        pygame.draw.rect(screen, color, die)

    # Aktualisierung des Bildschirms
    pygame.display.update()

    # Zeitverzögerung
    time.sleep(0.1)
