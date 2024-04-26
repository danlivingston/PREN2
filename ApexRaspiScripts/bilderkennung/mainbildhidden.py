import cv2
from ultralytics import YOLO
import os
import time
import subprocess

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Pfad für das zu startende Skript
first_script_path = os.path.join(base_dir, 'mainvisualbild.py')

# Pfad zum YOLOv8-Modell
model_path = os.path.join(base_dir, 'model', 'last.pt')

# Laden des YOLOv8-Modells
model = YOLO(model_path)

def open_camera_profile(ip_address, username, password, profile):
    # Starten des ersten Skripts
    first_script_process = subprocess.Popen(['python', first_script_path])
    
    # Video-Capture-Objekt für den RTSP-Stream
    cap = cv2.VideoCapture(f'rtsp://{username}:{password}@{ip_address}/axis-media/media.amp?streamprofile={profile}')
    if not cap.isOpened():
        print('Fehler: Der Video-Stream konnte nicht geöffnet werden.')
        # Beenden des zusätzlichen Skripts, falls ein Fehler auftritt
        first_script_process.terminate()
        return

    start_time = time.time()
    
    while True:
        if time.time() - start_time > 10:
            print('20 Sekunden sind vergangen, Programm wird beendet.')
            break
        
        ret, frame = cap.read()
        if not ret:
            print('Fehler: Es konnte kein Frame gelesen werden.')
            break
        
        results = model(frame)
        print(f'Anzahl der erkannten Objekte: {len(results)}')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

    # Beenden des zusätzlichen Skripts, wenn die Funktion endet
    first_script_process.terminate()
    try:
        # Warten auf das Beenden des zusätzlichen Skripts (mit Timeout)
        first_script_process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        # Erzwingen des Beendens, wenn das Skript nicht rechtzeitig beendet
        first_script_process.kill()

# Aufruf der Funktion zum Öffnen des RTSP-Streams und Anwenden der Objekterkennung
open_camera_profile('147.88.48.131', 'pren', '463997', 'pren_profile_med')
