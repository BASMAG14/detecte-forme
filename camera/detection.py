import cv2
import numpy as np

from utils.config import MIN_AREA, ROI_ENABLED, ROI_Y_MIN, ROI_Y_MAX


def find_objects(mask):

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    filtered = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        # حذف noise
        if area > MIN_AREA:
            # Si ROI activée, vérifier que le centre du contour est dans la bande verticale
            if ROI_ENABLED:
                x, y, w, h = cv2.boundingRect(cnt)
                cx = x + w // 2
                cy = y + h // 2
                h_img = mask.shape[0]
                y_min = int(ROI_Y_MIN * h_img)
                y_max = int(ROI_Y_MAX * h_img)
                if not (y_min <= cy <= y_max):
                    continue
            filtered.append(cnt)

    return filtered

# استخراج features
def extract_features(contour):

    # area
    area = cv2.contourArea(contour)

    # perimeter
    perimeter = cv2.arcLength(contour, True)

    # approximation polygon
    epsilon = 0.02 * perimeter

    approx = cv2.approxPolyDP(
        contour,
        epsilon,
        True
    )

    # corners
    corners = len(approx)

    # circularity
    circularity = 0

    if perimeter > 0:
        circularity = (
            4 * np.pi * area
        ) / (perimeter * perimeter)

    # bounding box
    x, y, w, h = cv2.boundingRect(contour)

    # ratio
    ratio = w / float(h)

    # center
    cx = x + w // 2
    cy = y + h // 2

    return {
        "area": area,
        "perimeter": perimeter,
        "corners": corners,
        "circularity": circularity,
        "bbox": (x, y, w, h),
        "ratio": ratio,
        "center": (cx, cy),
    }


# classification
def classify_shape(features):

    corners = features["corners"]
    ratio = features["ratio"]
    circularity = features["circularity"]
    area = features["area"]
    perimeter = features["perimeter"]

    # Prioritise clear circular shapes
    if circularity >= 0.65:
        return "CYLINDRE"

    # Triangle (explicit)
    if corners == 3:
        return "TRIANGLE"

    # Four corners -> treat as cube (inclut rectangles)
    if corners == 4:
        return "CUBE"

    # Polygons with many corners: decide between cylinder or cube
    if corners >= 5:
        if circularity >= 0.55:
            return "CYLINDRE"
        else:
            return "CUBE"

    # Fallback: use heuristics (no UNKNOWN)
    # If fairly circular -> cylinder, else cube
    if circularity >= 0.5:
        return "CYLINDRE"
    return "CUBE"