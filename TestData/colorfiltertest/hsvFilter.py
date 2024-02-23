import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture('/home/pi/TestData/cube_grgr-b-r.mp4') # Pfad zu Ihrem Video oder 0 für Webcam
    
    # Einstellung für Fenstergröße
    window_height = 480  # Neue Höhe
    window_width = 640   # Neue Breite
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Fenstergröße ändern
        frame_resized = cv2.resize(frame, (window_width, window_height))

        hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)
        
        # Weiß
        white_lower = np.array([5, 27, 214])
        white_upper = np.array([20, 165, 229])
        white_mask = cv2.inRange(hsv, white_lower, white_upper)
        white_res = cv2.bitwise_and(frame_resized, frame_resized, mask=white_mask)
        
        # Gelb
        yellow_lower = np.array([10, 137, 145])
        yellow_upper = np.array([20, 236, 237])
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
        yellow_res = cv2.bitwise_and(frame_resized, frame_resized, mask=yellow_mask)
        
        # Blau
        blue_lower = np.array([110, 57, 27])
        blue_upper = np.array([143, 132, 148])
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        blue_res = cv2.bitwise_and(frame_resized, frame_resized, mask=blue_mask)
        
        # Schwarz
        black_lower = np.array([3, 24, 24])
        black_upper = np.array([30, 168, 108])
        black_mask = cv2.inRange(hsv, black_lower, black_upper)
        black_res = cv2.bitwise_and(frame_resized, frame_resized, mask=black_mask)
        
        # Rot
        red_lower1 = np.array([0, 103, 90])
        red_upper1 = np.array([1, 195, 196])
        red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
        
        red_lower2 = np.array([177, 103, 90])
        red_upper2 = np.array([179, 195, 196])
        red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
        
        red_mask = red_mask1 | red_mask2
        red_res = cv2.bitwise_and(frame_resized, frame_resized, mask=red_mask)
        
        # Zeige die eingefärbten Masken
        cv2.imshow('frame', frame_resized)
        cv2.imshow('Yellow', white_res)
        cv2.imshow('White', white_res)
        cv2.imshow('Blue', blue_res)
        cv2.imshow('Black', black_res)
        cv2.imshow('Red', red_res)

        # Beende das Skript, wenn 'q' gedrückt wird
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

