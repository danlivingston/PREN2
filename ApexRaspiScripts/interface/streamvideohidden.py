import cv2
import time

def open_camera_profile(ip_address, username, password, profile):
    # Öffne die Kamera
    cap = cv2.VideoCapture('rtsp://' + username + ':' + password + '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', ip_address)
        return None

    frame_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Warning: unable to read next frame')
            break
        
        frame_count += 1
        
        # Hier kannst du Verarbeitung des Frames vornehmen
        
        # Gebe alle 5 Sekunden eine Nachricht aus
        if time.time() - start_time > 5:
            print(f'Running... Processed {frame_count} frames.')
            start_time = time.time()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Erlaubt es, das Programm mit 'q' zu beenden
            break

    # Gebe die Ressourcen frei und zerstöre alle geöffneten Fenster, wenn fertig
    cap.release()
    cv2.destroyAllWindows()

open_camera_profile('147.88.48.131', 'pren', '463997', 'pren_profile_med')

