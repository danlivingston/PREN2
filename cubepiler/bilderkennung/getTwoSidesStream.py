import os

import cv2
from loguru import logger
from ultralytics import YOLO

current_file_path = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file_path)

ip = os.getenv("STREAM_IP")
user = os.getenv("STREAM_USER")
pwd = os.getenv("STREAM_PWD")


class CubeFaceDetector:
    def __init__(
        self,
        model_path=f"{current_directory}/models/reference_segmentation_2.pt",
        ip_address=ip,
        username=user,
        password=pwd,
        profile="pren_profile_med",
    ):
        self.model = YOLO(model_path)
        self.imgWarmup = f"{current_directory}/warmup.jpg"
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.profile = profile

    async def warmupModels(self):
        warmupresultCube = self.model(self.imgWarmup)  # noqa: F841

    def delete_existing_files(self):
        files_to_delete = [
            f"{current_directory}/back_frame.jpg",
            f"{current_directory}/front_frame.jpg",
        ]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
                logger.trace(f"deleted {file}")

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

            if frame_counter % 14 == 0:
                results = self.model(frame)
                for r in results:
                    for box in r.boxes.xyxyn:  # Überprüfung aller Einträge
                        if box.shape[0] > 0:
                            logger.trace(box)
                            if (
                                not saved_front
                                and box[0] > 0.45
                                and box[1] > 0.358
                                and box[1] < 0.395
                            ):
                                cv2.imwrite(
                                    f"{current_directory}/front_frame.jpg", frame
                                )
                                logger.debug("saved front frame")
                                saved_front = True

                            if (
                                not saved_back
                                and box[0] < 0.43
                                and box[3] < 0.41
                                and box[3] > 0.375
                            ):
                                cv2.imwrite(
                                    f"{current_directory}/back_frame.jpg", frame
                                )
                                logger.debug("saved back frame")
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
