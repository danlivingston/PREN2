import time

import pygame

# Initialisierung von Pygame und Pygame Mixer
pygame.init()
pygame.mixer.init()

try:
    # Laden und Abspielen der Sounddatei 'piano.wav'
    sound = pygame.mixer.Sound("soundwindows.wav")
    sound.play()

    # Warten, bis der Ton abgespielt ist
    while pygame.mixer.get_busy():
        # Eine kleine Pause, um die CPU nicht zu überlasten
        time.sleep(0.1)

except pygame.error as e:
    print(f"Es gab einen Fehler beim Abspielen des Tons: {e}")

finally:
    # Pygame beenden
    pygame.quit()
