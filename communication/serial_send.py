import serial
import time

# Configuration du port série
SERIAL_PORT = 'COM3'  # À modifier selon votre port FPGA
BAUD_RATE = 9600

def init_serial():
    """Initialise la connexion série avec le FPGA"""
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connexion série établie sur {SERIAL_PORT}")
        return ser
    except serial.SerialException as e:
        print(f"Erreur de connexion série: {e}")
        return None

def send_signal(shape, ser=None):
    """Envoie le signal de forme détectée au FPGA"""

    # Mapping des formes vers les codes
    mapping = {
        "CUBE": b'1',
        "CYLINDRE": b'2',
        "TRIANGLE": b'3',
        "RECTANGLE": b'4',
        "UNKNOWN": b'0'
    }

    code = mapping.get(shape, b'0')

    if ser:
        try:
            ser.write(code)
            print(f"Signal envoyé au FPGA: {shape} -> {code.decode()}")
        except serial.SerialException as e:
            print(f"Erreur d'envoi série: {e}")
    else:
        # Mode simulation si pas de connexion série
        print(f"SIMULATION - Detected: {shape} -> Signal {code.decode()}")

# Instance globale de la connexion série
serial_connection = None

def initialize_fpga_connection():
    """Initialise la connexion FPGA au démarrage"""
    global serial_connection
    serial_connection = init_serial()
    return serial_connection

def send_to_fpga(shape):
    """Fonction principale pour envoyer au FPGA"""
    send_signal(shape, serial_connection)

# Test de transmission
def test_serial_send():
    """Teste l'envoi de données sur le port série"""
    ser = serial.Serial('COM3', 9600, timeout=1)
    for c in ['1','2','3']:
        ser.write(c.encode())
        print("envoyé", c)
        time.sleep(0.5)
    ser.close()