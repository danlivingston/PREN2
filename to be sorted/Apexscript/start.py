import tkinter as tk
import subprocess
import os
import pygame
import time

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Aufbau der Pfade relativ zum Basisverzeichnis
start_script_paths = [
    os.path.join(base_dir, 'codejson.py'), 
    os.path.join(base_dir, 'displayausgabe.py'),
    # Beispiel-Pfad, anpassen an die tatsächliche Struktur
    # Fügen Sie hier weitere Skripte hinzu, die beim Starten ausgeführt werden sollen
]
stop_script_path = os.path.join(base_dir, 'notausscript', 'abbruch.py')  # Beim Stoppen auszuführendes Skript

start_sound_path = os.path.join(base_dir, 'sound', 'startsignal.wav')  # Anpassen
stop_sound_path = os.path.join(base_dir, 'sound', 'stopsignal.wav')  # Anpassen

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
        process = subprocess.Popen(['python3', script_name], cwd=directory)
        processes.append(process)

def stop_files():
    global processes
    play_sound(stop_sound_path)
    # Beenden aller gestarteten Skripte
    for process in processes:
        try:
            process.terminate()
        except Exception as e:
            print(f"Fehler beim Beenden des Prozesses: {e}")
    processes = []  # Leeren der Liste nach dem Beenden der Prozesse
    # Starten des Abbruch-Skripts
    directory, script_name = os.path.split(stop_script_path)
    subprocess.Popen(['python3', script_name], cwd=directory)

# Einrichten des Hauptfensters
root = tk.Tk()
root.title("TALIS")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 2
window_height = screen_height
root.geometry(f'{window_width}x{window_height}+0+0')

frame = tk.Frame(root, bg='green')
frame.pack(expand=True, fill='both')

# Start- und Stopp-Button
start_button = tk.Button(frame, text="Start", command=lambda: start_files(start_script_paths), bg="green", fg="white", font=('Arial', 20))
start_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

stop_button = tk.Button(frame, text="Stop", command=stop_files, bg="red", fg="white", font=('Arial', 20))
stop_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

root.mainloop()
