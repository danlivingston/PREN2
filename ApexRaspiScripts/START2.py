import tkinter as tk
import subprocess
import os
import pygame
import time
import psutil

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

#beginn gleichzeitig
preparation_scripts = [
    os.path.join(base_dir, 'energiemessung', 'messung2.py'),
    os.path.join(base_dir, 'sound', 'startwavton.py'),
    # Weitere Skripte hier einfügen
]
 #seriell
core_script_paths = [
    os.path.join(base_dir, 'interface', 'getserverstate.py'),
    os.path.join(base_dir, 'interface', 'transmissionsignalstart.py'),
    os.path.join(base_dir, 'bilderkennung', 'mainbildhidden.py'),
    os.path.join(base_dir, 'interface', 'transscubeconfig.py'),
    os.path.join(base_dir, 'ansteuerungsprogramm2.py'),
    os.path.join(base_dir, 'visual', 'tischdownvisual2.py'),
    os.path.join(base_dir, 'interface', 'transmissionsignalstop.py')
    # Weitere Skripte hier einfügen oder dazwischen
]
#ende gleichzeitig
additional_script_paths = [
    os.path.join(base_dir, 'energiemessung', 'messungstopsignal.py'),
    os.path.join(base_dir, 'sound', 'endwavton.py'),
    os.path.join(base_dir, 'interface', 'getentries.py'),
    # Weitere zusätzliche Skripte hier einfügen
]

reset_script_paths = [
    os.path.join(base_dir, 'visual', 'resetvisual2.py'),
    os.path.join(base_dir, 'sound', 'resetwavton.py'),
    # Weitere Reset-Skripte hier einfügen
]

def start_files():
    start_button.config(state=tk.DISABLED)  # Deaktiviere den Start-Button sofort nach dem Klicken
    root.after(1500, lambda: start_button.config(state=tk.NORMAL))  # Reaktiviere den Button nach 1.5 Sekunden
    
    # Startet Vorbereitungsskripte asynchron
    for prep_script in preparation_scripts:
        prep_directory, prep_script_name = os.path.split(prep_script)
        subprocess.Popen(['python', prep_script_name], cwd=prep_directory)
    
    # Startet Hauptskripte synchron und prüft auf Erfolg
    for script in core_script_paths:
        directory, script_name = os.path.split(script)
        result = subprocess.run(['python', script_name], cwd=directory)
        if result.returncode != 0:
            print(f"Fehler beim Ausführen von {script_name}.")

    # Startet weitere Skripte asynchron
    for file_path in additional_script_paths:
        directory, script_name = os.path.split(file_path)
        subprocess.Popen(['python', script_name], cwd=directory)

def reset_files():
    reset_button.config(state=tk.DISABLED)  # Deaktiviere den Reset-Button sofort nach dem Klicken
    root.after(1500, lambda: reset_button.config(state=tk.NORMAL))  # Reaktiviere den Button nach 1.5 Sekunden
    
    # Startet Reset-Skripte asynchron
    for file_path in reset_script_paths:
        directory, script_name = os.path.split(file_path)
        subprocess.Popen(['python', script_name], cwd=directory)

def stop_files():
    # Spielt den Stop-Ton ab
    sound_script_path = os.path.join(base_dir, 'sound', 'stopwavton.py')
    subprocess.Popen(['python', sound_script_path])

    current_process_pid = os.getpid()  # PID des aktuellen (dieses) Prozesses

    # Erstelle eine Liste von Skriptnamen statt vollständigen Pfaden
    script_names_to_stop = [os.path.basename(script) for script in
                            core_script_paths + additional_script_paths + reset_script_paths + preparation_scripts]

    for process in psutil.process_iter(['pid', 'cmdline']):
        try:
            if 'python' in ' '.join(process.info['cmdline']).lower() and process.info['pid'] != current_process_pid:
                # Überprüfe, ob einer der Skriptnamen in den Befehlszeilenargumenten vorkommt
                if any(script_name in ' '.join(process.info['cmdline']) for script_name in script_names_to_stop):
                    process.terminate()  # Beenden des Prozesses
                    print(f"Terminated process PID={process.info['pid']} with cmdline={process.info['cmdline']}")
        except Exception as e:
            print(f"Error terminating process PID={process.info['pid']}: {e}")

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