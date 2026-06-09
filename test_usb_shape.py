#!/usr/bin/env python3
"""Test rapide: caméra USB + détection de formes."""

import sys
import time

import cv2

from camera.capture import init_camera, capture_frame, get_active_camera_info
from camera.preprocess import preprocess
from camera.detection import find_objects, extract_features, classify_shape


def test_detection(cap, live=False):
    print("\n=== Test détection de formes (caméra USB) ===")
    print("Placez des objets (cube, cylindre, triangle) devant la caméra.")
    if live:
        print("Fenêtre ouverte — 'q' quitter, 's' sauvegarder.")
    else:
        print("Capture d'une frame de test...")

    frame_count = 0
    fail_count = 0

    while True:
        frame = capture_frame(cap)
        if frame is None:
            fail_count += 1
            if fail_count >= 30:
                print("\nErreur: trop d'échecs de capture.")
                print("→ Rebranchez la caméra USB et relancez le script.")
                return 1
            if fail_count == 1:
                print("Attente image caméra", end="", flush=True)
            elif fail_count % 5 == 0:
                print(".", end="", flush=True)
            time.sleep(0.1)
            continue

        fail_count = 0
        gray, blurred, binary, eroded, cleaned = preprocess(frame)
        contours = find_objects(cleaned)
        display = frame.copy()

        shapes = []
        for cnt in contours:
            features = extract_features(cnt)
            shape = classify_shape(features)
            shapes.append(shape)

            x, y, w, h = features["bbox"]
            cx, cy = features["center"]
            cv2.drawContours(display, [cnt], -1, (0, 255, 0), 2)
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 255), 1)
            cv2.circle(display, (cx, cy), 4, (255, 0, 0), -1)
            cv2.putText(display, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        frame_count += 1
        cam = get_active_camera_info()
        cam_label = cam.get("name", "camera")
        is_builtin = cam.get("is_builtin", False)
        info = f"Objets: {len(contours)} | Formes: {', '.join(shapes) if shapes else 'aucune'}"
        cam_info = f"Camera: {cam_label}" + (" [WEBCAM PC - pas USB]" if is_builtin else " [USB]")
        cv2.putText(display, cam_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        cv2.putText(display, info, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        if not live:
            print(info)
            cv2.imwrite("test_detection_frame.jpg", display)
            print("Image sauvegardée: test_detection_frame.jpg")
            break

        window_title = f"Detection - {cam_label}"
        cv2.imshow(window_title, display)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("s"):
            fname = f"capture_{frame_count}.jpg"
            cv2.imwrite(fname, display)
            print(f"Sauvegardé: {fname}")

    return 0


def main():
    live = "--live" in sys.argv
    use_hp = "--hp" in sys.argv

    print("=" * 50)
    print("  TEST CAMERA - DETECTION DE FORMES")
    print("=" * 50)
    if use_hp:
        print("Mode: webcam HP (secours)\n")

    try:
        cap = init_camera(allow_builtin=use_hp)
    except Exception as e:
        print(f"\nERREUR: {e}")
        print("\n--- QUE FAIRE ? ---")
        print("1. Branchez la camera USB (LED allumee)")
        print("2. Attendez 5 secondes")
        print("3. Relancez: python test_usb_shape.py --live")
        print("")
        print("OU utilisez la webcam HP en secours:")
        print("   python test_usb_shape.py --live --hp")
        return 1

    try:
        return test_detection(cap, live=live)
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
