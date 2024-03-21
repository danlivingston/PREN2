import tkinter as tk
import subprocess
import os
import pygame
import time

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Aufbau der Pfade relativ zum Basisverzeichnis
start_script_paths = [
    os.path.join(base_dir, 'interface', 'transmissionsignalstart.py'), 
    os.path.join(base_dir, 'bilderkennung', 'segmentation_yolo.py'),
    os.path.join(base_dir, 'codejson.py'), 
]
stop_script_path = os.path.join(base_dir, 'notausscript', 'reboot.py')  # Beim Stoppen auszuführendes Skript (ausgeklammert für diesen Fall)

start_sound_path = os.path.join(base_dir, 'sound', 'startsignal.wav')  # Anpassen
# stop_sound_path = os.path.join(base_dir, 'sound', 'stopsignal.wav')  # Ausgeklammert für diesen Fall

processes = []

def play_sound(sound_path):
    pygame.init()
    pygame.mixer.init()
    try:
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
        while pygame.mixer.get_busy():
            time.sleep(0.1)
    except pygame.error as e:
        print(f"Es gab einen Fehler beim Abspielen des Tons: {e}")
    finally:
        pygame.quit()

def start_files(file_paths):
    global processes
    play_sound(start_sound_path)
    for file_path in file_paths:
        directory, script_name = os.path.split(file_path)
        process = subprocess.Popen(['python', script_name], cwd=directory)
        processes.append(process)

# Die Funktion stop_files() und alles damit Verbundene wird für diesen Fall nicht benötigt.

# Einrichten des Hauptfensters
root = tk.Tk()
root.title("TALIS")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width
window_height = screen_height
root.geometry(f'{window_width}x{window_height}+0+0')

# Ein einzelner Frame, der den gesamten Bildschirm einnimmt, und grün ist
frame = tk.Frame(root, bg='green')
frame.pack(fill='both', expand=True)

# Ein "Start"-Knopf, der den gesamten Bildschirm einnimmt
start_button = tk.Button(frame, text="Start", command=lambda: start_files(start_script_paths), bg="green", fg="white", font=('Arial', 20))
start_button.pack(fill='both', expand=True)

root.mainloop()
