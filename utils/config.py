# couleurs

SHAPE_COLORS = {

    "CUBE": (0,255,0),

    "CYLINDRE": (255,0,0),

    "TRIANGLE": (0,0,255),

    "RECTANGLE": (255,255,0),

    "UNKNOWN": (0,255,255),
}

# configuration de la caméra
USB_CAMERA_NAME = "USB2.0 Camera"  # Nom de la caméra USB externe (DirectShow)
BUILTIN_CAMERA_NAME = "HP HD Camera"  # Webcam intégrée (secours)
USB_CAMERA_INDEX = None  # Laisser None = sélection auto (ignore la webcam intégrée)
CAMERA_SCAN_MAX = 8
CAMERA_WARMUP_FRAMES = 30  # Frames à ignorer au démarrage (caméra USB lente)

# Caméras intégrées du PC à ignorer
BUILTIN_CAMERA_PATTERNS = [
    "HP HD Camera",
    "HP IR Camera",
    "Integrated",
    "IR Camera",
    "Facetime",
    "Built-in",
]

# minimum area
MIN_AREA = 1200

# ROI (region of interest) pour se concentrer sur le tapis roulant
# Si ROI_ENABLED=True, seules les contours dont le centre est dans
# la bande verticale [ROI_Y_MIN, ROI_Y_MAX] (fraction de la hauteur)
# seront considérés.
ROI_ENABLED = False
ROI_Y_MIN = 0.40  # start fraction from top (0.0) -> 40% down
ROI_Y_MAX = 0.95  # end fraction from top (0.0) -> 95% down