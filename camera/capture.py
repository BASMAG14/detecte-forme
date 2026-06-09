import sys
import time

import cv2

from utils.config import (
    USB_CAMERA_INDEX,
    USB_CAMERA_NAME,
    BUILTIN_CAMERA_NAME,
    CAMERA_SCAN_MAX,
    BUILTIN_CAMERA_PATTERNS,
    CAMERA_WARMUP_FRAMES,
)


active_camera_info = {"name": "", "index": 0, "is_builtin": False}


def get_active_camera_info():
    return active_camera_info.copy()


def open_camera(index, backend=cv2.CAP_DSHOW):
    """Ouvre la caméra avec un backend Windows."""
    try:
        cap = cv2.VideoCapture(index, backend)
        if cap.isOpened():
            return cap
    except Exception:
        pass
    return cv2.VideoCapture(index)


def _list_dshow_devices():
    try:
        from pygrabber.dshow_graph import FilterGraph

        return FilterGraph().get_input_devices()
    except Exception:
        return None


def _is_builtin_camera(name):
    name_lower = name.lower()
    return any(pattern.lower() in name_lower for pattern in BUILTIN_CAMERA_PATTERNS)


def _print_detected_devices(devices):
    print("Caméras détectées:")
    for i, name in enumerate(devices):
        kind = "intégrée (ignorée)" if _is_builtin_camera(name) else "USB"
        print(f"  [{i}] {name} ({kind})")


def resolve_usb_camera(allow_builtin=False):
    """
    Trouve la caméra USB externe et ignore la webcam intégrée du PC.
    Si allow_builtin=True, utilise HP HD Camera en secours.
    Retourne (index, nom). Ne ouvre pas la caméra ici.
    """
    devices = _list_dshow_devices()
    if devices:
        _print_detected_devices(devices)

        if USB_CAMERA_NAME:
            for i, name in enumerate(devices):
                if USB_CAMERA_NAME.lower() in name.lower() and not _is_builtin_camera(name):
                    return i, name

        for i, name in enumerate(devices):
            if not _is_builtin_camera(name):
                return i, name

        if allow_builtin:
            for i, name in enumerate(devices):
                if BUILTIN_CAMERA_NAME.lower() in name.lower():
                    print(f"\nMode secours: utilisation de {name}")
                    return i, name
            print(f"\nMode secours: utilisation de {devices[0]}")
            return 0, devices[0]

        if all(_is_builtin_camera(name) for name in devices):
            raise Exception(
                "Seule la webcam integree du PC est disponible.\n"
                f"Branchez la camera USB '{USB_CAMERA_NAME}' et reessayez.\n"
                "OU lancez avec --hp pour utiliser la webcam HP temporairement."
            )
        raise Exception("Caméra USB externe introuvable.")

    candidates = []
    for i in range(CAMERA_SCAN_MAX):
        cap = open_camera(i)
        if cap.isOpened():
            candidates.append(i)
        cap.release()

    if not candidates:
        raise Exception("Aucune caméra détectée.")

    if USB_CAMERA_INDEX is not None and USB_CAMERA_INDEX in candidates:
        return USB_CAMERA_INDEX, f"index {USB_CAMERA_INDEX}"

    if len(candidates) >= 2:
        chosen = max(candidates)
        return chosen, f"index {chosen}"

    if len(candidates) == 1 and candidates[0] == 0:
        raise Exception(
            "Seule la webcam integree (index 0) est disponible.\n"
            f"Branchez la camera USB '{USB_CAMERA_NAME}'."
        )

    return candidates[0], f"index {candidates[0]}"


def _warmup_camera(cap, frames=CAMERA_WARMUP_FRAMES):
    for _ in range(frames):
        cap.read()


def _try_open_with_backend(index, backend):
    cap = open_camera(index, backend)
    if not cap.isOpened():
        return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    try:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    except Exception:
        pass

    _warmup_camera(cap)

    for _ in range(15):
        ret, frame = cap.read()
        if ret and frame is not None and frame.size > 0:
            backend_name = cap.getBackendName() if hasattr(cap, "getBackendName") else str(backend)
            print(f"Caméra prête ({backend_name})")
            return cap
        time.sleep(0.05)

    cap.release()
    return None


def init_camera(index=None, allow_builtin=False):
    """Ouvre la caméra une seule fois, avec plusieurs tentatives."""
    camera_name = f"index {index}" if index is not None else ""

    if index is None:
        chosen, camera_name = resolve_usb_camera(allow_builtin=allow_builtin)
        label = "SECOURS (webcam PC)" if allow_builtin and _is_builtin_camera(camera_name) else "USB"
        print(f"Camera active [{label}]: {camera_name} (index {chosen})")
        index = chosen

    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]

    for attempt in range(3):
        if attempt > 0:
            print(f"Nouvelle tentative ({attempt + 1}/3)...")
            time.sleep(1.0)

        for backend in backends:
            cap = _try_open_with_backend(index, backend)
            if cap is not None:
                active_camera_info["name"] = camera_name
                active_camera_info["index"] = index
                active_camera_info["is_builtin"] = _is_builtin_camera(camera_name)
                return cap

    raise Exception(
        "La camera USB est detectee mais ne renvoie pas d'image.\n"
        "1) Debranchez la camera, attendez 10 secondes, rebranchez sur un autre port USB.\n"
        "2) Fermez Zoom/Teams si ouverts.\n"
        "3) Lancez: powershell -ExecutionPolicy Bypass -File repair_usb_camera.ps1"
    )


def choose_camera_index(candidates, default=None):
    if not candidates:
        return None

    if default in candidates:
        print(f"Utilisation du port USB configuré: index={default}")
        return default

    print("Indices de caméras disponibles:", candidates)
    if sys.stdin is not None and sys.stdin.isatty():
        choice = input(
            "Entrez l'index de la caméra USB à utiliser "
            "(laisser vide pour choisir le plus élevé) : "
        ).strip()
        if choice.isdigit():
            return int(choice)

    chosen = max(candidates)
    print(f"Aucun index configuré valide, utilisation de l'index le plus élevé: {chosen}")
    return chosen


def capture_frame(cap, target_width=960, retries=10):
    for _ in range(retries):
        ret, frame = cap.read()
        if ret and frame is not None and frame.size > 0:
            h, w = frame.shape[:2]
            if w > target_width:
                scale = target_width / float(w)
                frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
            return frame
        time.sleep(0.05)
    return None
