import os

import cv2
from loguru import logger
from ultralytics import YOLO

current_file_path = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file_path)


class CubeFaceDetector:
    def __init__(
        self,
        model_path=f"{current_directory}/models/reference_segmentation_2.pt",
        ip_address=os.getenv("STREAM_IP"),
        username=os.getenv("STREAM_USER"),
        password=os.getenv("STREAM_PWD"),
        profile="pren_profile_med",
    ):
        self.model = YOLO(model_path)
        self.imgWarmup = f"{current_directory}/warmup.jpg"
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.profile = profile

    async def warmupModels(self):
        warmupresultCube = self.model(self.imgWarmup)

    def delete_existing_files(self):
        files_to_delete = [
            f"{current_directory}/back_frame.jpg",
            f"{current_directory}/front_frame.jpg",
        ]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)

    def open_camera_profile(self):
        self.delete_existing_files()

        cap = cv2.VideoCapture(
            f"rtsp://{self.username}:{self.password}@{self.ip_address}/axis-media/media.amp?streamprofile={self.profile}"
        )

        if not cap.isOpened():
            raise Exception("Der Video-Stream konnte nicht geöffnet werden.")

        frame_counter = 0
        saved_front = False
        saved_back = False

        while True:
            ret, frame = cap.read()
            frame_counter += 1

            if not ret:
                raise Exception("Es konnte kein Frame gelesen werden.")

            if frame_counter % 15 == 0:
                results = self.model(frame)
                for r in results:
                    if r.boxes.xyxyn.shape[0] > 0:
                        logger.trace(r.boxes.xyxyn)
                        if (
                            not saved_front
                            and r.boxes.xyxyn[0][0] > 0.35
                            and r.boxes.xyxyn[0][1] > 0.35
                        ):
                            cv2.imwrite(f"{current_directory}/front_frame.jpg", frame)
                            saved_front = True

                        if (
                            not saved_back
                            and r.boxes.xyxyn[0][2] < 0.65
                            and r.boxes.xyxyn[0][3] < 0.41
                        ):
                            cv2.imwrite(f"{current_directory}/back_frame.jpg", frame)
                            saved_back = True

                        if saved_front and saved_back:
                            cap.release()
                            cv2.destroyAllWindows()
                            return

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    async def start_detection(self):
        self.open_camera_profile()