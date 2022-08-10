import cv2
camera = cv2.VideoCapture(2)
while True:
    success, frame = camera.read()  # read the camera frame
    if not success:
        break
    else:
        print(frame)
print(camera.isOpened())