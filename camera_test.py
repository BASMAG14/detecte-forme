import cv2

from camera.capture import init_camera, capture_frame

cap = init_camera()

while True:
    frame = capture_frame(cap)

    if frame is None:
        print("Camera error")
        break

    cv2.imshow("Camera Test (USB only)", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
