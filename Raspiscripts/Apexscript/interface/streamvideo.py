import cv2

def open_camera_profile(ip_address, username, password, profile):
    # Open the camera
    cap = cv2.VideoCapture('rtsp://' + username + ':' + password + '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', ip_address)
        return None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Warning: unable to read next frame')
            break
        
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

open_camera_profile('147.88.48.131', 'pren', '463997', 'pren_profile_small')
