import cv2
import numpy as np

# Pfad zur Videodatei
video_path = "/home/pi/TestData/cube_grgr-b-r.mp4"

# VideoCapture Objekt erstellen
cap = cv2.VideoCapture(video_path)

# Farbbereiche definieren
color_ranges = {
    "red": ((0, 120, 70), (10, 255, 255), (0, 0, 255)),  # Farbbereich, Farbe der Kontur
    "blue": ((100, 150, 0), (170, 255, 255), (255, 0, 0)),
    "yellow": ((15, 100, 100), (35, 255, 255), (0, 255, 255)),
    "white": ((0, 0, 200), (180, 20, 255), (255, 255, 255)),
}


def process_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color, (
        (lower_h, lower_s, lower_v),
        (upper_h, upper_s, upper_v),
        contour_color,
    ) in color_ranges.items():
        mask = cv2.inRange(
            hsv, (lower_h, lower_s, lower_v), (upper_h, upper_s, upper_v)
        )
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Konturen zeichnen
        for contour in contours:
            approx = cv2.approxPolyDP(
                contour, 0.02 * cv2.arcLength(contour, True), True
            )
            cv2.drawContours(
                frame, [approx], 0, contour_color, -1
            )  # -1 füllt die Kontur aus

    return frame


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = process_frame(frame)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
