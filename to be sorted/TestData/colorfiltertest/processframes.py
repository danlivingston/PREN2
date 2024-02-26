import cv2

# Pfad zur Videodatei
video_path = "/home/pi/TestData/cube_-b-r-b-r.mp4"

# VideoCapture Objekt erstellen
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    # Frame einlesen
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Hier können Sie den Frame verarbeiten, z.B. mit Bildverarbeitungstechniken

    # Frame anzeigen
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
