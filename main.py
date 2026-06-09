import time
import cv2

# import fonctions dyalna
from camera.capture import init_camera, capture_frame
from camera.preprocess import preprocess
from camera.detection import (
    find_objects,
    extract_features,
    classify_shape
)

from communication.serial_send import initialize_fpga_connection, send_to_fpga
from utils.config import SHAPE_COLORS


def main():

    # Initialiser la connexion FPGA
    print("Initialisation de la connexion FPGA...")
    fpga_connected = initialize_fpga_connection()

    # تشغيل الكاميرا
    cap = init_camera()

    # حساب FPS
    prev_time = time.time()

    # boucle infinie
    while True:

        # أخذ صورة من الكاميرا
        frame = capture_frame(cap)

        # إذا الصورة غير موجودة
        if frame is None:
            print("Frame introuvable, réinitialisation de la caméra...")
            cap.release()
            cap = init_camera()
            continue

        # traitement image
        gray, blurred, binary, eroded, cleaned = preprocess(frame)

        # استخراج objects
        contours = find_objects(cleaned)

        # نسخة للرسم
        display = frame.copy()

        # loop sur objets
        for contour in contours:

            # استخراج الخصائص
            features = extract_features(contour)

            # classification
            shape = classify_shape(features)

            # اللون
            color = SHAPE_COLORS.get(shape)

            # position
            x, y, w, h = features["bbox"]

            # center
            cx, cy = features["center"]

            # رسم contour
            cv2.drawContours(display, [contour], -1, color, 2)

            # rectangle
            cv2.rectangle(display, (x, y), (x+w, y+h), color, 2)

            # center point
            cv2.circle(display, (cx, cy), 4, color, -1)

            # text
            cv2.putText(
                display,
                shape,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            # إرسال signal لل FPGA
            send_to_fpga(shape)

        # حساب FPS
        current_time = time.time()

        fps = 1.0 / max(current_time - prev_time, 1e-6)

        prev_time = current_time

        # afficher FPS
        cv2.putText(
            display,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        # afficher fenêtre
        cv2.imshow("FPGA CAMERA PROJECT", display)

        # quitter
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # fermer camera
    cap.release()

    cv2.destroyAllWindows()


# point entrée
if __name__ == "__main__":
    main()