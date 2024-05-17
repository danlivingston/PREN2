import cv2
from ultralytics import YOLO
import os


def open_camera_profile(ip_address, username, password, profile):
    model = YOLO("ApexRaspiScripts/bilderkennung/models/reference_segmentation_2.pt")

    cap = cv2.VideoCapture(
        f"rtsp://{username}:{password}@{ip_address}/axis-media/media.amp?streamprofile={profile}"
    )

    if not cap.isOpened():
        print("Fehler: Der Video-Stream konnte nicht geöffnet werden.")
        return

    frame_counter = 0
    saved_front = False
    saved_back = False

    while True:
        ret, frame = cap.read()
        frame_counter += 1

        if not ret:
            print("Fehler: Es konnte kein Frame gelesen werden.")
            break

        if frame_counter % 11 == 0:
            results = model(frame)
            for r in results:
                if r.boxes.xyxyn.shape[0] > 0:
                    print(r.boxes.xyxyn)
                    if (
                        not saved_front
                        and r.boxes.xyxyn[0][0] > 0.35
                        and r.boxes.xyxyn[0][1] > 0.35
                    ):
                        cv2.imwrite("front_frame.jpg", frame)
                        saved_front = True

                    if (
                        not saved_back
                        and r.boxes.xyxyn[0][2] < 0.65
                        and r.boxes.xyxyn[0][3] < 0.43
                    ):
                        cv2.imwrite("back_frame.jpg", frame)
                        saved_back = True

                    if saved_front and saved_back:
                        print("Beide Bilder wurden gespeichert. Beenden der Schleife.")
                        cap.release()
                        cv2.destroyAllWindows()
                        return

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# open_camera_profile("147.88.48.131", "pren", "463997", "pren_profile_med")
