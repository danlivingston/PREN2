import cv2
import numpy as np

# Video laden
cap = cv2.VideoCapture("/home/pi/TestData/cube_grgr-b-r.mp4")


def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Wenn Maus geklickt wird
        pixel = frame_hsv[y, x]  # Hole HSV-Werte des Pixels
        print(f"HSV Value at {x}, {y} is {pixel}")


cv2.namedWindow("frame")
cv2.setMouseCallback("frame", pick_color)  # Setze Maus Callback

paused = False
while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break  # Wenn keine Frames mehr vorhanden sind, beende die Schleife

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(
        " "
    ):  # Wenn Leertaste gedrückt wird, schalte zwischen Pause und Play um
        paused = not paused
    elif key == ord("q"):  # Wenn 'q' gedrückt wird, beende die Schleife
        break

cap.release()
cv2.destroyAllWindows()
