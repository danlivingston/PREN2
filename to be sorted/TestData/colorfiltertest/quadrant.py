import cv2
import numpy as np


def is_line_through_center(x1, y1, x2, y2, centerX, centerY, marginX, marginY):
    if x2 - x1 == 0:  # Um Division durch Null zu vermeiden
        return lowerBoundX <= x1 <= upperBoundX
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1  # y = mx + c => c = y - mx
    y_at_centerX = slope * centerX + intercept
    x_at_centerY = (centerY - intercept) / slope
    return (lowerBoundY <= y_at_centerX <= upperBoundY) and (
        lowerBoundX <= x_at_centerY <= upperBoundX
    )


cap = cv2.VideoCapture("/home/pi/TestData/cube_grgr-b-r.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    centerX, centerY = width // 2, height // 2

    marginX, marginY = width * 0.1, height * 0.1
    lowerBoundX, upperBoundX = centerX - marginX, centerX + marginX
    lowerBoundY, upperBoundY = centerY - marginY, centerY + marginY

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10
    )

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if is_line_through_center(
                x1, y1, x2, y2, centerX, centerY, marginX, marginY
            ):
                cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
