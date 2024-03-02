import datetime

import pygame

# Pygame initialisieren
pygame.init()

# Bildschirmeinstellungen
screen_width, screen_height = 800, 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Konfigurationsanzeige")

# Farben definieren
colors = {
    "yellow": (255, 255, 0),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "grey": (200, 200, 200),  # Grau für leere Zustände
}

# Konfigurationsdaten
config_data = {
    "1": "yellow",
    "2": "red",
    "3": "grey",
    "4": "blue",
    "5": "yellow",
    "6": "red",
    "7": "grey",
    "8": "blue",
}


# Funktion zum Anzeigen der Konfiguration
def display_config(time, config, step):
    screen.fill((0, 0, 0))  # Bildschirm mit Schwarz füllen
    font = pygame.font.Font(None, 36)

    # Zeit anzeigen
    time_text = font.render(time, True, (255, 255, 255))
    screen.blit(time_text, (10, 10))

    # Jeden Konfigurationsstatus anzeigen
    for i, (key, value) in enumerate(config.items()):
        # Wenn der Schritt kleiner als die Blocknummer ist, zeige Grau an, sonst die definierte Farbe
        color = colors[value] if int(key) <= step else colors["grey"]
        pygame.draw.rect(screen, color, (50 * i + 50, 100, 40, 40))
        text = font.render(key, True, (255, 255, 255))
        screen.blit(text, (50 * i + 50, 150))

    # "Fertig" rechts neben den Würfeln anzeigen, wenn der letzte Schritt erreicht ist
    if step >= len(config_data):
        finished_text = font.render("Fertig", True, (0, 255, 0))
        screen.blit(finished_text, (50 * len(config_data) + 50, 100))

    pygame.display.flip()


# Schleife, um die Animation zu zeigen
current_time = "2023-11-15 21:09:05"
step = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Zeit aktualisieren und Anzeige aktualisieren
    current_time = (
        datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        + datetime.timedelta(seconds=1)
    ).strftime("%Y-%m-%d %H:%M:%S")
    display_config(current_time, config_data, step)
    step += 1

    if step <= len(config_data):
        pygame.time.wait(1000)  # Warte eine Sekunde zwischen jedem Schritt

# Pygame beenden
pygame.quit()
