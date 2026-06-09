import cv2

try:
    from pygrabber.dshow_graph import FilterGraph

    device_names = FilterGraph().get_input_devices()
except Exception:
    device_names = []


def camera_name(index):
    if index < len(device_names):
        return device_names[index]
    return "inconnue"


print("Scan des cameras...")
print("=" * 60)
if device_names:
    print("Noms DirectShow:")
    for i, name in enumerate(device_names):
        print(f"  [{i}] {name}")
    print()

for i in range(8):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"INDEX {i}: non disponible")
        cap.release()
        continue

    ret, frame = cap.read()
    if not ret or frame is None:
        print(f"INDEX {i}: ouverte mais pas d'image")
        cap.release()
        continue

    h, w = frame.shape[:2]
    name = camera_name(i)
    is_usb = "USB2.0" in name or "USB" in name.upper()
    kind = "USB EXTERNE" if is_usb else "webcam PC"

    print(f"\nINDEX {i}: OK - {name} ({kind})")
    print(f"  Resolution: {w}x{h}")

    label = f"Index {i} - {name}"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow(label, frame)
    print("  Fenetre affichee 3 secondes...")
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    cap.release()

print("\n" + "=" * 60)
print("Pour ce PC:")
for i, name in enumerate(device_names):
    if "USB" in name.upper() and "HP" not in name:
        print(f"  Camera USB = index {i} ({name})")
print("\nLancez: python test_usb_shape.py --live")
