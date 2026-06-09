#!/usr/bin/env python3
"""
Version simplifiée du système FPGA Camera
Fonctionne sans FPGA physique - simulation complète
"""

import time
import sys
import cv2
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Import des modules existants
from camera.capture import init_camera, capture_frame
from camera.preprocess import preprocess
from camera.detection import find_objects, extract_features, classify_shape
from utils.config import SHAPE_COLORS

class VirtualFPGA:
    """Simulation FPGA avec interface graphique"""

    def __init__(self):
        self.current_shape = "UNKNOWN"
        self.led_states = {
            "CUBE": False,
            "CYLINDRE": False,
            "TRIANGLE": False,
            "RECTANGLE": False,
            "UNKNOWN": True
        }

        # Créer l'interface graphique
        self.create_gui()

    def create_gui(self):
        """Crée l'interface graphique pour simuler le FPGA"""
        self.root = tk.Tk()
        self.root.title("FPGA Simulator - Virtual LEDs")
        self.root.geometry("400x300")

        # Titre
        title = ttk.Label(self.root, text="FPGA Shape Detector", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Frame pour les LEDs
        led_frame = ttk.LabelFrame(self.root, text="LED Status", padding=10)
        led_frame.pack(pady=10, padx=20, fill="x")

        # LEDs virtuelles
        self.led_labels = {}
        self.shape_labels = {}

        shapes = ["CUBE", "CYLINDRE", "TRIANGLE", "RECTANGLE", "UNKNOWN"]
        colors = ["red", "blue", "green", "yellow", "gray"]

        for i, (shape, color) in enumerate(zip(shapes, colors)):
            # Label de forme
            shape_label = ttk.Label(led_frame, text=f"{shape}:", font=("Arial", 10, "bold"))
            shape_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            # LED simulée (cercle coloré)
            led_label = tk.Label(led_frame, text="●", font=("Arial", 24), fg="gray")
            led_label.grid(row=i, column=1, padx=10, pady=5)

            self.led_labels[shape] = led_label
            self.shape_labels[shape] = shape_label

        # Label pour afficher la forme actuelle
        self.status_label = ttk.Label(self.root, text="Current Shape: UNKNOWN",
                                    font=("Arial", 12), foreground="blue")
        self.status_label.pack(pady=10)

        # Bouton de reset
        reset_btn = ttk.Button(self.root, text="Reset LEDs", command=self.reset_leds)
        reset_btn.pack(pady=5)

    def update_leds(self, shape):
        """Met à jour les LEDs selon la forme détectée"""
        if shape != self.current_shape:
            self.current_shape = shape

            # Reset all LEDs
            for s in self.led_states:
                self.led_states[s] = False
                self.led_labels[s].config(fg="gray")

            # Turn on the detected shape LED
            if shape in self.led_states:
                self.led_states[shape] = True
                color = {"CUBE": "red", "CYLINDRE": "blue", "TRIANGLE": "green", "RECTANGLE": "yellow", "UNKNOWN": "orange"}[shape]
                self.led_labels[shape].config(fg=color)

            # Update status
            self.status_label.config(text=f"Current Shape: {shape}")

            print(f"FPGA Simulation: {shape} detected - LED {shape} ON")

    def reset_leds(self):
        """Remet toutes les LEDs à l'état éteint"""
        for shape in self.led_states:
            self.led_states[shape] = False
            self.led_labels[shape].config(fg="gray")
        self.current_shape = "UNKNOWN"
        self.status_label.config(text="Current Shape: UNKNOWN")
        print("FPGA Simulation: All LEDs reset")

    def start_gui(self):
        """Démarre l'interface graphique"""
        self.root.mainloop()

def camera_loop(fpga, allow_builtin=False):
    """Boucle de traitement de la caméra dans un thread séparé"""
    # Initialiser la caméra
    print("Initialisation de la caméra...")
    cap = init_camera(allow_builtin=allow_builtin)

    # Variables FPS
    prev_time = time.time()

    print("Système prêt ! Placez des objets devant la caméra.")
    print("Appuyez sur 'q' pour quitter.")
    print()

    # Boucle principale
    while True:
        # Capturer une frame
        frame = capture_frame(cap)
        if frame is None:
            print("Frame introuvable, réinitialisation de la caméra...")
            cap.release()
            cap = init_camera(allow_builtin=allow_builtin)
            continue

        # Prétraitement
        gray, blurred, binary, eroded, cleaned = preprocess(frame)

        # Détection d'objets
        contours = find_objects(cleaned)

        # Copie pour affichage
        display = frame.copy()

        # Traiter chaque objet détecté
        detected_shapes = []
        for contour in contours:
            features = extract_features(contour)
            shape = classify_shape(features)

            # Couleur selon la forme
            color = SHAPE_COLORS.get(shape, (255, 255, 255))

            # Position
            x, y, w, h = features["bbox"]
            cx, cy = features["center"]

            # Dessiner
            cv2.drawContours(display, [contour], -1, color, 2)
            cv2.rectangle(display, (x, y), (x+w, y+h), color, 2)
            cv2.circle(display, (cx, cy), 4, color, -1)
            cv2.putText(display, shape, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            detected_shapes.append(shape)

            # Envoyer au FPGA simulé
            fpga.update_leds(shape)

        # Calculer FPS
        current_time = time.time()
        fps = 1.0 / max(current_time - prev_time, 1e-6)
        prev_time = current_time

        # Afficher FPS
        cv2.putText(display, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        # Afficher nombre d'objets
        cv2.putText(display, f"Objects: {len(contours)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        # Afficher la fenêtre
        cv2.imshow("FPGA Camera Project - Simulation Mode", display)

        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Nettoyage
    cap.release()
    cv2.destroyAllWindows()
    print("\nSystème arrêté.")

def main():
    """Fonction principale avec simulation FPGA"""
    use_hp = "--hp" in sys.argv

    print("=== FPGA Camera Project - Mode Simulation ===")
    if use_hp:
        print("Mode secours: webcam HP")
    print("Démarrage du simulateur FPGA virtuel...")
    print()

    # Créer le simulateur FPGA
    fpga = VirtualFPGA()

    # Démarrer la boucle caméra dans un thread séparé
    camera_thread = Thread(target=camera_loop, args=(fpga, use_hp), daemon=True)
    camera_thread.start()

    # Démarrer l'interface graphique dans le thread principal
    fpga.start_gui()

if __name__ == "__main__":
    main()