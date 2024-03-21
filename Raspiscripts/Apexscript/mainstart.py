import tkinter as tk
import subprocess
import os
import pygame
import time
import psutil  # Für das Verwalten von Prozessen

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Pfad für das zuerst auszuführende Skript und das zweite wichtige Skript
first_script_path = os.path.join(base_dir, 'interface', 'getserverstate.py')
second_script_path = os.path.join(base_dir, 'interface', 'transmissionsignalstart.py')

# Aufbau der Pfade relativ zum Basisverzeichnis für die nachfolgenden Skripte
additional_script_paths = [
    os.path.join(base_dir, '3ansteuerungsprogramm3.py'), 
    os.path.join(base_dir, 'bilderkennung', 'probestreamerkennung.py'),
]

start_sound_path = os.path.join(base_dir, 'sound', 'startsignal.wav')
stop_sound_path = os.path.join(base_dir, 'sound', 'stopsignal.wav')

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

def start_files():
    # Deaktiviere nur den Start-Button sofort nach dem Klicken
    start_button.config(state=tk.DISABLED)
    
    play_sound(start_sound_path)
    
    # Führe das erste Skript synchron aus und prüfe auf Erfolg
    first_directory, first_script_name = os.path.split(first_script_path)
    result_first = subprocess.run(['python', first_script_name], cwd=first_directory)
    if result_first.returncode != 0:
        print(f"Fehler beim Ausführen von {first_script_name}.")
    
    # Führe das zweite Skript synchron aus und prüfe auf Erfolg
    second_directory, second_script_name = os.path.split(second_script_path)
    result_second = subprocess.run(['python', second_script_name], cwd=second_directory)
    if result_second.returncode != 0:
        print(f"Fehler beim Ausführen von {second_script_name}.")
    
    # Führe die restlichen Skripte asynchron aus, unabhängig vom Erfolg der ersten beiden
    print("Starte weitere Skripte.")
    for file_path in additional_script_paths:
        directory, script_name = os.path.split(file_path)
        subprocess.Popen(['python', script_name], cwd=directory)
    
    # Setze einen Timer, um den Start-Button nach 2 Sekunden wieder zu aktivieren
    root.after(2000, lambda: start_button.config(state=tk.NORMAL))

def stop_files():
    play_sound(stop_sound_path)
    current_process_pid = os.getpid()  # PID des aktuellen (dieses) Prozesses

    for process in psutil.process_iter(attrs=['pid', 'cmdline']):
        try:
            if process.info['cmdline'] and "python" in process.info['cmdline'][0] and process.info['pid'] != current_process_pid:
                script_path = process.info['cmdline'][1] if len(process.info['cmdline']) > 1 else ""
                if any(script_path.endswith(os.path.basename(script)) for script in additional_script_paths + [first_script_path, second_script_path]):
                    psutil.Process(process.info['pid']).terminate()
        except Exception as e:
            print(f"Fehler beim Beenden des Prozesses: {e}")
            
# Einrichten des Hauptfensters und des restlichen UI bleibt unverändert
root = tk.Tk()
root.title("TALIS")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width
window_height = screen_height
root.geometry(f'{window_width}x{window_height}+0+0')

left_frame = tk.Frame(root, bg='green')
left_frame.pack(side=tk.LEFT, fill='both', expand=True)

right_frame = tk.Frame(root, bg='red')
right_frame.pack(side=tk.RIGHT, fill='both', expand=True)

start_button = tk.Button(left_frame, text="Start", command=start_files, bg="green", fg="white", font=('Arial', 20))
start_button.pack(fill='both', expand=True)

stop_button = tk.Button(right_frame, text="Stop", command=stop_files, bg="red", fg="white", font=('Arial', 20))
stop_button.pack(fill='both', expand=True)

root.mainloop()
