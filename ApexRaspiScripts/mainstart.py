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
    os.path.join(base_dir, 'bilderkennung', 'probestreamerkennung.py'),
    os.path.join(base_dir, 'zRaspiscripts', 'probeansteurungsprogramm', '3ansteuerungsprogramm3.py'), 
]

reset_script_paths = [
    os.path.join(base_dir, 'mainreset.py'),
    #Zusätzliche Scripte
]


start_sound_path = os.path.join(base_dir, 'sound', 'startsignal.wav')
stop_sound_path = os.path.join(base_dir, 'sound', 'stopsignal.wav')
reset_sound_path = os.path.join(base_dir, 'sound', 'reset.wav')

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
    
def reset_files():
    play_sound(reset_sound_path)
    
    # Iterieren durch alle Pfade in der reset_script_paths Liste
    for script_path in reset_script_paths:
        directory, script_name = os.path.split(script_path)
        result = subprocess.run(['python', script_name], cwd=directory)
        if result.returncode != 0:
            print(f"Fehler beim Ausführen von {script_name}.")
            
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
            
root = tk.Tk()
root.title("TALIS")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width
window_height = screen_height
root.geometry(f'{window_width}x{window_height}+0+0')

# Teilen des linken Frames in zwei Unter-Frames
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill='both', expand=True)

upper_left_frame = tk.Frame(left_frame, bg='yellow')
upper_left_frame.pack(side=tk.TOP, fill='both', expand=True)

lower_left_frame = tk.Frame(left_frame, bg='green')
lower_left_frame.pack(side=tk.BOTTOM, fill='both', expand=True)

right_frame = tk.Frame(root, bg='red')
right_frame.pack(side=tk.RIGHT, fill='both', expand=True)

# Positionieren des Reset-Buttons im oberen linken Frame
reset_button = tk.Button(upper_left_frame, text="Reset", command=reset_files, bg="orange", fg="white", font=('Arial', 50))
reset_button.pack(fill='both', expand=True)

# Positionieren des Start-Buttons im unteren linken Frame
start_button = tk.Button(lower_left_frame, text="Start", command=start_files, bg="green", fg="white", font=('Arial', 50))
start_button.pack(fill='both', expand=True)

# Stop-Button im rechten Frame
stop_button = tk.Button(right_frame, text="Stop", command=stop_files, bg="red", fg="white", font=('Arial', 50))
stop_button.pack(fill='both', expand=True)

root.mainloop()