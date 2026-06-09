# Projet FPGA Camera - Détection d'Objets

Ce projet combine la vision par ordinateur Python avec un FPGA pour la détection et le traitement en temps réel de formes géométriques.

## Architecture du Système

```
[Caméra USB] → [Python + OpenCV] → [Port Série] → [FPGA] → [LEDs/Actionneurs]
```

## Composants Matériels Nécessaires

1. **Caméra USB** - Pour la capture vidéo
2. **Carte FPGA** (ex: DE10-Nano, Cyclone V, etc.)
3. **Convertisseur USB vers UART** (FTDI, CP2102, etc.)
4. **LEDs** - Pour indiquer les formes détectées
5. **Câbles de connexion**

## Configuration Logicielle

### 1. Installation des Dépendances Python

```bash
pip install opencv-python numpy pyserial
```

### 2. Configuration du Port Série

Dans `communication/serial_send.py`, modifiez :
```python
SERIAL_PORT = 'COM3'  # Remplacez par votre port COM
BAUD_RATE = 9600
```

Pour trouver le port COM sous Windows :
- Ouvrez le Gestionnaire de périphériques
- Cherchez "Ports (COM et LPT)"
- Notez le numéro du port de votre convertisseur USB-UART

## Connexions Matérielles

### FPGA ↔ Convertisseur UART

| FPGA Pin | UART Module | Description |
|----------|-------------|-------------|
| RX       | TX         | Réception des données |
| GND      | GND        | Masse commune |

### FPGA ↔ LEDs

| FPGA Pin | LED | Description |
|----------|-----|-------------|
| led_cube     | LED1 | S'allume pour les cubes |
| led_cylinder | LED2 | S'allume pour les cylindres |
| led_triangle | LED3 | S'allume pour les triangles |
| led_unknown  | LED4 | S'allume pour formes inconnues |

## Utilisation

### 1. Programmer le FPGA

1. Ouvrez Quartus Prime (ou votre logiciel FPGA)
2. Créez un nouveau projet
3. Ajoutez le fichier `fpga_shape_detector.vhd`
4. Configurez les contraintes selon votre carte FPGA
5. Compilez et programmez le FPGA

### 2. Lancer l'Application Python

```bash
python main.py
```

### 3. Test du Système

1. Placez des objets devant la caméra :
   - **Cube** : Objet carré/rectangulaire
   - **Cylindre** : Objet circulaire
   - **Triangle** : Objet triangulaire

2. Observez :
   - La détection en temps réel dans la fenêtre Python
   - Les LEDs correspondantes qui s'allument sur le FPGA

## Codes de Communication

| Forme | Code ASCII | Signal Binaire | Action FPGA |
|-------|------------|----------------|-------------|
| Cube  | '1' (49)  | 00110001      | LED Cube ON |
| Cylindre | '2' (50) | 00110010      | LED Cylindre ON |
| Triangle | '3' (51) | 00110011      | LED Triangle ON |
| Inconnu | '0' (48) | 00110000      | LED Unknown ON |

## Dépannage

### Problèmes Courants

1. **Port série non trouvé**
   - Vérifiez le numéro du port COM
   - Assurez-vous que le convertisseur USB-UART est connecté

2. **FPGA ne reçoit pas les données**
   - Vérifiez les connexions RX/TX
   - Vérifiez la vitesse de baud (9600)
   - Vérifiez l'horloge du FPGA

3. **LEDs ne s'allument pas**
   - Vérifiez les connexions des LEDs
   - Vérifiez la logique du FPGA

### Mode Simulation

Si le FPGA n'est pas connecté, le programme fonctionne en mode simulation :
- Les signaux sont affichés dans la console Python
- Aucune connexion série n'est requise

## Extension du Système

### Ajouter de Nouvelles Formes

1. Modifiez le mapping dans `communication/serial_send.py`
2. Ajoutez la logique de décodage dans le VHDL
3. Ajoutez les LEDs correspondantes

### Actions Plus Complexes

Au lieu d'allumer des LEDs, le FPGA peut :
- Contrôler des moteurs
- Activer des relais
- Générer des signaux PWM
- Communiquer avec d'autres périphériques

## Schéma de Connexion

```
[Ordinateur USB] → [Caméra USB]
                    ↓
[Python OpenCV] → [Traitement d'image]
                    ↓
[Port COM] → [USB-UART] → [FPGA RX Pin]
                              ↓
[FPGA] → [LEDs pour chaque forme]
```

## Fichiers du Projet

- `main.py` - Application principale Python
- `camera/capture.py` - Capture vidéo
- `camera/preprocess.py` - Prétraitement d'image
- `camera/detection.py` - Détection et classification
- `communication/serial_send.py` - Communication série
- `fpga_shape_detector.vhd` - Logique FPGA VHDL
- `fpga_constraints.qsf` - Contraintes FPGA