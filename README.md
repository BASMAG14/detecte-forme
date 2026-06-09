# FPGA Camera Project - Guide Complet

## 🎯 Démarrage Rapide

### Option 1 : Mode Simulation (Recommandé - Pas de Quartus requis)
```bash
python launcher.py
# Choisissez 1
```

### Option 2 : Mode FPGA Réel (Nécessite Quartus)
```bash
python launcher.py
# Choisissez 2
```

## 📋 Modes Disponibles

### 🎮 Mode Simulation
- **Interface graphique** avec LEDs virtuelles
- **Aucun matériel FPGA** nécessaire
- **Test complet** sans installation de Quartus
- **Parfait pour** découvrir et développer

### 🔧 Mode FPGA Réel
- **Communication série** réelle
- **VHDL sur FPGA** physique
- **LEDs matérielles** contrôlées
- **Nécessite** Quartus Prime

## 🛠️ Installation

### Dépendances de Base
```bash
pip install opencv-python numpy pyserial
```

### Pour FPGA Réel Seulement
- Quartus Prime (gratuit pour FPGA Intel)
- Carte FPGA (DE10-Nano, Cyclone V, etc.)
- Convertisseur USB-UART

## 🎯 Utilisation

### Mode Simulation
1. `python launcher.py` → Option 1
2. Placez objets devant caméra
3. Observez LEDs virtuelles

### Mode FPGA Réel
1. **Programmez FPGA :**
   - Ouvrez `fpga_shape_detector.vhd` dans Quartus
   - Compilez et programmez

2. **Connectez :**
   - Caméra USB → PC
   - USB-UART → COM3
   - FPGA RX → UART TX

3. **Lancez :**
   - `python launcher.py` → Option 2

## 📊 Codes de Formes

| Forme | Signal | Action |
|-------|--------|---------|
| Cube | '1' | LED Rouge |
| Cylindre | '2' | LED Bleue |
| Triangle | '3' | LED Verte |
| Inconnu | '0' | LED Orange |

## 📁 Structure du Projet

```
FPGA_Camera_Project/
├── launcher.py              # Menu principal
├── main.py                  # Mode FPGA réel
├── main_simulation.py       # Mode simulation
├── test_fpga_communication.py
├── camera/                  # Vision par ordinateur
├── communication/           # Interface série
├── utils/                   # Configuration
├── fpga_shape_detector.vhd  # Code VHDL
├── fpga_constraints.qsf     # Pins FPGA
└── README.md               # Cette documentation
```

## 🔧 Dépannage

### Caméra
- **Erreur caméra :** Vérifiez permissions et connexion USB
- **Mauvaise caméra :** Le système détecte automatiquement la caméra USB

### Mode Simulation
- **Interface ne s'affiche pas :** `pip install tk` (si nécessaire)

### Mode FPGA
- **Port COM :** Modifiez `SERIAL_PORT` dans `serial_send.py`
- **Pas de signal :** Vérifiez connexions UART et programmation FPGA

## 🚀 Pour Commencer

**Lancez simplement :**
```bash
python launcher.py
```

Choisissez le **Mode Simulation** pour découvrir le système sans matériel FPGA !

---

*Le Mode Simulation permet de tester complètement la vision par ordinateur et la logique de détection sans avoir besoin de Quartus ou de matériel FPGA.*