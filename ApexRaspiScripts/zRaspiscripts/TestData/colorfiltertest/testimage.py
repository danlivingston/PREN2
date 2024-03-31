from time import sleep

import picamera2

# Initialisieren der Kamera
camera = picamera2.PiCamera()

# Aufnahme eines Bildes
camera.capture("testbild.jpg")
