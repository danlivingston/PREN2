import picamera2
from time import sleep

# Initialisieren der Kamera
camera = picamera2.PiCamera()

# Aufnahme eines Bildes
camera.capture('testbild.jpg')
