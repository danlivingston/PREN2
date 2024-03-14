import cv2
from ultralytics import YOLO
import os

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Korrekter Pfad zum YOLOv8-Modell, relativ zum Basisverzeichnis
model_path = os.path.join(base_dir, "model", "last.pt")

# Laden des YOLOv8-Modells
model = YOLO(model_path)


def open_camera_profile(ip_address, username, password, profile):
    # Öffnen des Video-Capture-Objekts für den RTSP-Stream
    cap = cv2.VideoCapture(
        f"rtsp://{username}:{password}@{ip_address}/axis-media/media.amp?streamprofile={profile}"
    )

    # Überprüfen, ob das Video-Capture-Objekt erfolgreich geöffnet wurde
    if not cap.isOpened():
        print("Fehler: Der Video-Stream konnte nicht geöffnet werden.")
        return

    annotated_frame = None
    frame_counter = -1

    # Schleife durch die Frames des Video-Streams
    while True:
        # Ein Frame aus dem Video lesen
        ret, frame = cap.read()

        # Überprüfen, ob ein Frame erfolgreich gelesen wurde
        if not ret:
            print("Fehler: Es konnte kein Frame gelesen werden.")
            break

        frame_counter += 1

        if (frame_counter % 10) == 0:
            # Objekterkennung auf dem Frame durchführen
            results = model(frame)

            # Visualisieren der erkannten Objekte auf dem Frame
            annotated_frame = results[0].plot()

        # Frame mit den erkannten Objekten anzeigen
        cv2.imshow("YOLOv8 Object Detection", annotated_frame)

        # Warten auf Tastenanschlag ('q' zum Beenden)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Video-Capture-Objekt freigeben und das Anzeigefenster schließen
    cap.release()
    cv2.destroyAllWindows()


# Aufruf der Funktion zum Öffnen des RTSP-Streams und Anwenden der Objekterkennung
open_camera_profile("147.88.48.131", "pren", "463997", "pren_profile_med")

# open_camera_profile('147.88.48.131', 'pren', '463997', 'pren_profile_small')
