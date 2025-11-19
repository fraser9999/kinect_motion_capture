

### **README.md**

````markdown
# Kinect v1 Motion Capture Python Project

**Author:** Hermann Knopp  
**Date:** 17.06.2025  
**Python Version:** 3.10.10  
**Stage:** Early Alpha  

---

## Projektübersicht

Dieses Projekt ermöglicht die **Aufnahme, Visualisierung und Konvertierung von Motion Capture Daten** mit einer **Kinect v1 Tiefenkamera** unter Windows. Die aufgenommenen Rohdaten können anschließend in das **BVH-Format** konvertiert werden, das für Animationen in Blender verwendet werden kann.

Das Projekt ist in drei Hauptmodule unterteilt:

1. **Rohdaten aufnehmen** – `Kinect_Recorder.py`  
   Liest die Kinect-Daten aus, verfolgt das Skelett und speichert die XYZ-Koordinaten jedes Gelenks in einer Textdatei.

2. **Visualisieren & Überprüfen** – `Kinect_Anim_plotter.py`  
   Lädt die gespeicherten Rohdaten und stellt sie als **3D-Linienanimation** dar, um die Qualität der erfassten Bewegungen zu überprüfen.

3. **Konvertieren in BVH** – `BVH_Writer.py`  
   Wandelt die Rohdaten in **Blender-kompatible BVH-Dateien** um, inkl. Berechnung von Gelenkrotationen.

---

## Voraussetzungen

### Software
- **Kinect SDK 1.8** (für Kinect V1 Unterstützung)  
- **OpenNI2** (`Openni_x64.exe`)  
- **NiTE2** (`Nite2_x64.exe`)  

### Wichtige Dateien
- `h.dat` und `s.dat` müssen im **Application-Verzeichnis** vorhanden sein oder korrekt im Systempfad liegen.

### Systempfad
- OpenNI2 und NiTE2 müssen im Systempfad (`PATH`) registriert sein.  
- Optional: `nite2.dll` und `openni2.dll` können in den Python App-Ordner kopiert werden.

---

## Installation

1. Python 3.10.10 installieren.  
2. Virtuelle Umgebung erstellen:
   ```bash
   python -m venv venv
   venv\Scripts\activate
````

3. Benötigte Python-Pakete installieren:

   ```bash
   pip install -r requirements.txt
   ```
4. Kinect SDK, OpenNI2, NiTE2 installieren.
5. Sicherstellen, dass die Daten-Dateien (`h.dat`, `s.dat`) erreichbar sind.


Download:

"Openni_x64.exe"  
OpenNI-Windows-x64-2.2.0.33.zip (from structure.io or openni.com website)

"Nite2_x64.exe"
NiTE2-Windows-x64(x86)-2.21.zip (from openni.com website)

Kinect SDK 1.7 or 1.8
(from microsoft.com)



---

## Nutzung

### 1. Rohdaten aufnehmen

```bash
python Kinect_Recorder.py -o output_file.txt
```

* Startet die Kinect-Skelettverfolgung.
* Speichert Rohdaten der Gelenke in einer Textdatei (`output_file.txt`).
* Mit `q` kann die Aufnahme beendet werden.

### 2. Visualisierung der Daten

```bash
python Kinect_Anim_plotter.py
```

* Eingabe des Pfads zur gespeicherten Rohdaten-Datei.
* Zeigt eine 3D-Linienanimation der aufgenommenen Frames an.

### 3. BVH-Datei erzeugen

```bash
python BVH_Writer.py
```

* Eingabe des Pfads zur Rohdaten-Datei.
* Erstellt eine Blender-kompatible `.bvh` Datei im Projektordner.

---

## Projektstruktur

```
/project_root
│
├─ Kinect_Recorder.py      # Rohdatenaufnahme von Kinect
├─ Kinect_Anim_plotter.py  # 3D-Visualisierung
├─ BVH_Writer.py           # BVH Konvertierung
├─ requirements.txt        # Python-Abhängigkeiten
└─ README.md
```

---

## Python-Abhängigkeiten

* `numpy`
* `opencv-python`
* `matplotlib`
* `scipy`
* `openni` (Python-Bindings für OpenNI2/NiTE2)

---

## Hinweise

* Bei Startproblemen überprüfen:

  * Liegen `h.dat` und `s.dat` im richtigen Verzeichnis?
  * Sind `openni2.dll` und `nite2.dll` verfügbar?
  * Wurde der Systempfad korrekt gesetzt?

````

---

### **requirements.txt**

```text
numpy>=1.23
opencv-python>=4.7
matplotlib>=3.7
scipy>=1.11
openni>=2.2.0
````

