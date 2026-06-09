import cv2
import numpy as np

def preprocess(frame):

    frame = cv2.resize(frame, (640,480))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (7,7), 0)

    # Adaptive threshold + Otsu to handle variable lighting
    adaptive = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    _, otsu = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Edge-based mask to improve contour extraction
    edges = cv2.Canny(blurred, 50, 150)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)

    combined = cv2.bitwise_or(adaptive, otsu)
    combined = cv2.bitwise_or(combined, edges)

    kernel = np.ones((5,5), np.uint8)

    cleaned = cv2.morphologyEx(
        combined,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    cleaned = cv2.morphologyEx(
        cleaned,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )

    return gray, blurred, combined, edges, cleaned