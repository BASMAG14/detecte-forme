#!/usr/bin/env python3
"""
Lanceur du Projet FPGA Camera
Permet de choisir entre mode réel FPGA et mode simulation
"""

import sys
import os

def print_menu():
    """Affiche le menu principal"""
    print("=== FPGA Camera Project ===")
    print()
    print("Choisissez le mode d'exécution :")
    print("1. Mode Simulation (sans FPGA - recommandé pour commencer)")
    print("2. Mode FPGA Réel (nécessite Quartus et matériel FPGA)")
    print("3. Test Communication FPGA (test des signaux)")
    print("4. Test caméra + détection (--hp si USB ne marche pas)")
    print("5. Quitter")
    print()

def main():
    while True:
        print_menu()
        try:
            choice = input("Votre choix (1-5) : ").strip()

            if choice == "1":
                print("\nDémarrage du mode simulation...")
                print("Ce mode utilise une interface graphique pour simuler le FPGA")
                print("Pas besoin de Quartus ou de matériel FPGA !")
                print()
                os.system("python main_simulation.py")

            elif choice == "2":
                print("\nDémarrage du mode FPGA réel...")
                print("Assurez-vous que votre FPGA est programmé avec fpga_shape_detector.vhd")
                print("et connecté au port série configuré (COM3 par défaut)")
                print()
                input("Appuyez sur Entrée pour continuer...")
                os.system("python main.py")

            elif choice == "3":
                print("\nTest de la communication FPGA...")
                os.system("python test_fpga_communication.py")
                input("\nAppuyez sur Entrée pour continuer...")

            elif choice == "4":
                print("\nTest caméra et détection de formes...")
                print("Si la caméra USB ne marche pas, tapez: hp")
                cam = input("Appuyez Entrée (USB) ou tapez 'hp' (webcam HP): ").strip().lower()
                flag = " --live --hp" if cam == "hp" else " --live"
                os.system(f"python test_usb_shape.py{flag}")
                input("\nAppuyez sur Entrée pour continuer...")

            elif choice == "5":
                print("\nAu revoir !")
                sys.exit(0)

            else:
                print("\nChoix invalide. Veuillez choisir 1, 2, 3, 4 ou 5.")
                input("Appuyez sur Entrée pour continuer...")

        except KeyboardInterrupt:
            print("\n\nInterruption détectée. Au revoir !")
            sys.exit(0)
        except Exception as e:
            print(f"\nErreur : {e}")
            input("Appuyez sur Entrée pour continuer...")

        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()