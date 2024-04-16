import os
import pygame

def play_sound(sound_file):
    # Initialisiere Pygame
    pygame.init()

    # Lade den Sound
    sound = pygame.mixer.Sound(sound_file)

    # Spiele den Sound ab
    sound.play()

    # Warte, bis der Sound abgespielt wurde
    while pygame.mixer.get_busy():
        pygame.time.delay(10)  # Warte 100 Millisekunden

if __name__ == "__main__":
    # Bestimme den Basisordner, in dem sich das Skript befindet
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Erstelle den vollständigen Pfad zur Sounddatei
    sound_file = os.path.join(base_dir, 'startsignal.wav')  # Ersetze 'your_soundfile.wav' mit dem Namen deiner Sounddatei

    # Spiele den Sound ab
    play_sound(sound_file)
