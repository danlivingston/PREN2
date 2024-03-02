import cv2
import cv2 as cv
import imutils
import numpy as np

color = (255, 255, 255)
# I have defined lower and upper boundaries for each color for my camera
# Strongly recommended finding for your own camera.
colors = {
    "blue": [np.array([80, 50, 50]), np.array([140, 255, 255])],
    "red": [np.array([0, 50, 50]), np.array([20, 255, 255])],
    #'white': [np.array([0, 0, 160]), np.array([180, 30, 255])],
    "yellow": [np.array([10, 50, 50]), np.array([50, 255, 255])],
}


def find_color(frame, points):
    mask = cv.inRange(frame, points[0], points[1])  # create mask with boundaries
    cnts = cv.findContours(
        mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
    )  # find contours from mask
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        area = cv.contourArea(c)  # find how big countour is
        if area > 5000:  # only if countour is big enough, then
            M = cv.moments(c)
            cx = int(M["m10"] / M["m00"])  # calculate X position
            cy = int(M["m01"] / M["m00"])  # calculate Y position
            return c, cx, cy


cap = cv.VideoCapture(0)


# Funktion zur Erkennung der Würfel und Markierung
def detect_and_mark_cubes(frame):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # convertion to HSV
    for name, clr in colors.items():  # for each color in colors
        if find_color(hsv, clr):  # call find_color function above
            c, cx, cy = find_color(hsv, clr)
            cv.drawContours(frame, [c], -1, color, 1)  # draw contours
            cv.circle(frame, (cx, cy), 7, color, -1)  # draw circle
            cv.putText(
                frame, name, (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 1, color, 1
            )  # put text
    return frame


# Öffne das Videofile
# video_capture = cv2.VideoCapture('cube_slow_2.mkv')
video_capture = cv2.VideoCapture("cube_fast_1.mkv")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Verarbeite das Frame, um Würfel zu erkennen und zu markieren
    processed_frame = detect_and_mark_cubes(frame)

    # Zeige das verarbeitete Frame
    cv2.imshow("Video mit erkannten Würfeln", processed_frame)

    # Beenden mit der Taste 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Freigeben der Ressourcen
video_capture.release()
cv2.destroyAllWindows()
