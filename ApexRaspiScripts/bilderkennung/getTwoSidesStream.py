import cv2
from ultralytics import YOLO
from quarter import Quarter
from circle import Circle
import os


class CubeFaceDetector:
    def __init__(self, model_path='ApexRaspiScripts/bilderkennung/models/reference_segmentation_2.pt', ip_address="147.88.48.131", username="pren", password="463997", profile="pren_profile_med"):
        self.model = YOLO(model_path)
        self.imgWarmup = 'warmup.jpg'
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.profile = profile

    def warmupModels(self):
        warmupresultCube = self.model(self.imgWarmup)
    def delete_existing_files(self):
        files_to_delete = ['back_frame.jpg', 'front_frame.jpg']
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)

    def open_camera_profile(self):
        self.delete_existing_files()

        cap = cv2.VideoCapture(
            f"rtsp://{self.username}:{self.password}@{self.ip_address}/axis-media/media.amp?streamprofile={self.profile}"
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

            if frame_counter % 8 == 0:
                results = self.model(frame)
                for r in results:
                    if r.boxes.xyxyn.shape[0] > 0:
                        print(r.boxes.xyxyn)
                        if not saved_front and r.boxes.xyxyn[0][0] > 0.35 and r.boxes.xyxyn[0][1] > 0.35:
                            cv2.imwrite('front_frame.jpg', frame)
                            saved_front = True

                        if not saved_back and r.boxes.xyxyn[0][2] < 0.65 and r.boxes.xyxyn[0][3] < 0.41:
                            cv2.imwrite('back_frame.jpg', frame)
                            saved_back = True

                        if saved_front and saved_back:
                            cap.release()
                            cv2.destroyAllWindows()
                            return

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def start_detection(self):
        self.open_camera_profile()


#detector = CubeFaceDetector()
#detector.warmupModels()
#detector.start_detection()
