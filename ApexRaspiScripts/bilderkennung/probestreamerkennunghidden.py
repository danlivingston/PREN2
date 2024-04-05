import cv2
from ultralytics import YOLO
import os
import time  # Importiere die time-Bibliothek

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Korrekter Pfad zum YOLOv8-Modell, relativ zum Basisverzeichnis
model_path = os.path.join(base_dir, 'model', 'last.pt')

# Laden des YOLOv8-Modells
model = YOLO(model_path)

def open_camera_profile(ip_address, username, password, profile):
    # Öffnen des Video-Capture-Objekts für den RTSP-Stream
    cap = cv2.VideoCapture(f'rtsp://{username}:{password}@{ip_address}/axis-media/media.amp?streamprofile={profile}')

    # Überprüfen, ob das Video-Capture-Objekt erfolgreich geöffnet wurde
    if not cap.isOpened():
        print('Fehler: Der Video-Stream konnte nicht geöffnet werden.')
        return

    start_time = time.time()  # Startzeit markieren

    # Schleife durch die Frames des Video-Streams
    while True:
        # Überprüfen, ob 20 Sekunden vergangen sind
        if time.time() - start_time > 20:
            print('20 Sekunden sind vergangen, Programm wird beendet.')
            break

        # Ein Frame aus dem Video lesen
        ret, frame = cap.read()

        # Überprüfen, ob ein Frame erfolgreich gelesen wurde
        if not ret:
            print('Fehler: Es konnte kein Frame gelesen werden.')
            break

        # Objekterkennung auf dem Frame durchführen
        results = model(frame)

        # Verarbeitung und Ausgabe der Ergebnisse
        print(f'Anzahl der erkannten Objekte: {len(results)}')

        # Warten auf Tastenanschlag ('q' zum Beenden), auch wenn kein Fenster angezeigt wird
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Video-Capture-Objekt freigeben und das Anzeigefenster schließen
    cap.release()
    cv2.destroyAllWindows()

# Aufruf der Funktion zum Öffnen des RTSP-Streams und Anwenden der Objekterkennung
open_camera_profile('147.88.48.131', 'pren', '463997', 'pren_profile_med')
