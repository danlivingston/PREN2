import cv2
from ultralytics import YOLO
import os

# Ermitteln des Basisverzeichnisses relativ zum aktuellen Skript
base_dir = os.path.dirname(os.path.abspath(__file__))

# Korrekter Pfad zum YOLOv8-Modell, relativ zum Basisverzeichnis
model_path = os.path.join(base_dir, 'model', 'last.pt')

# Load the YOLOv8 model
model = YOLO(model_path)

# Korrekter Pfad zur Videodatei, relativ zum Basisverzeichnis
video_path = os.path.join(base_dir, "pren_cube_01.mp4")
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()  # Behält die ursprüngliche Methode zur Visualisierung bei

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
