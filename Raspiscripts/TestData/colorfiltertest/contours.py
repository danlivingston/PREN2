import cv2
import numpy as np

cap = cv2.VideoCapture("/home/pi/TestData/cube_grgr-b-r.mp4")

# Bereich für den weißen Quadranten
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 25, 255])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Bild in HSV umwandeln
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Maskierung des weißen Quadranten
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    # Finde Konturen
    contours, _ = cv2.findContours(
        mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        if (
            cv2.contourArea(contour) > 500
        ):  # Filterkonturen nach Größe, 500 ist nur ein Beispielwert
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(
                frame, (x, y), (x + w, y + h), (0, 255, 0), 2
            )  # Zeichne Rechtecke um die Konturen

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
