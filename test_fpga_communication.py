#!/usr/bin/env python3
"""
Test script pour la communication FPGA
Démontre l'envoi de signaux de formes au FPGA
"""

from communication.serial_send import initialize_fpga_connection, send_to_fpga
import time

def test_fpga_communication():
    """Test complet de la communication FPGA"""

    print("=== Test Communication FPGA ===")
    print()

    # Initialisation
    print("1. Initialisation de la connexion FPGA...")
    fpga_connection = initialize_fpga_connection()

    if fpga_connection:
        print("   OK - Connexion FPGA etablie")
    else:
        print("   Mode simulation (pas de FPGA connecte)")

    print()

    # Test des différentes formes
    shapes_to_test = ["CUBE", "CYLINDRE", "TRIANGLE", "UNKNOWN"]

    print("2. Test d'envoi des signaux de formes :")
    print()

    for shape in shapes_to_test:
        print(f"   Envoi signal pour : {shape}")
        send_to_fpga(shape)
        time.sleep(0.5)  # Pause entre les envois

    print()
    print("3. Test terminé !")
    print()
    print("Codes de formes :")
    print("   CUBE     -> Signal '1' -> LED Cube")
    print("   CYLINDRE -> Signal '2' -> LED Cylindre")
    print("   TRIANGLE -> Signal '3' -> LED Triangle")
    print("   UNKNOWN  -> Signal '0' -> LED Unknown")

if __name__ == "__main__":
    test_fpga_communication()