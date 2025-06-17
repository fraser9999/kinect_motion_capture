# Hermanns Kinect to BVH Converter
# 2025/6/16
# Early Alpha
# python 3.10.10 x64
 

# Init

import os
os.system("cls")
print("importing libs....")

# Librarys

import numpy as np
from scipy.spatial.transform import Rotation as R
from datetime import datetime

# --- Hierarchie der Gelenke ---

hierarchy = {
    'Hip': ['ShoulderCenter', 'HipLeft', 'HipRight'],
    'ShoulderCenter': ['Head', 'ShoulderLeft', 'ShoulderRight'],
    # not used today 
    #'Torso': ['ShoulderCenter'],
    'ShoulderLeft': ['ElbowLeft'],
    'ElbowLeft': ['WristLeft'],
    'ShoulderRight': ['ElbowRight'],
    'ElbowRight': ['WristRight'],
    'HipLeft': ['KneeLeft'],
    'KneeLeft': ['AnkleLeft'],
    'HipRight': ['KneeRight'],
    'KneeRight': ['AnkleRight'],
}

# --- Hilfsfunktionen ---

# Skalierungsfaktor
SCALE_FACTOR = 1

# Anpassung der Positionen während des Lesens
def read_frames_from_file(filename):
    frames = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        frame = {}
        joint_name = None  # Gelenkname wird hier gesetzt

        for line in lines:
            line = line.strip()
            if line == '':
                if frame:
                    frames.append(frame)
                frame = {}
                joint_name = None
            else:
                parts = line.split()
                
                if len(parts) == 7:  # Wir erwarten 7 Werte (Name + 6 Koordinaten)
                    joint_name = parts[0]  # Gelenkname extrahieren
                    # Extrahieren der Positionen (x1, y1, z1) und (x2, y2, z2)
                    position_1 = tuple(map(float, parts[1:4]))  # x1, y1, z1
                    position_2 = tuple(map(float, parts[4:7]))  # x2, y2, z2

                    # Skalierung der Positionen
                    position_1 = tuple(np.array(position_1) * SCALE_FACTOR)
                    position_2 = tuple(np.array(position_2) * SCALE_FACTOR)

                    # Speichern der Positionen unter dem Gelenknamen
                    frame[joint_name] = (position_1, position_2)  # Parent- und Child-Position

                else:
                    print(f"Unerwartetes Format: {line}")
                    return []  # Fehler bei der Formatierung, Rückgabe einer leeren Liste

        if frame:  # Die letzte Zeile hinzufügen, wenn sie nicht leer ist
            frames.append(frame)
    
    return frames



# Normalize Vectors

def normalize(v):
    """Normalisiere einen Vektor"""
    norm = np.linalg.norm(v)
    if norm == 0:
        #print("V: ",str(v))
        #a=input("wait key")        
        return v
    else: 
        v= v / norm
        #print("V-Norm: ",str(v))
        #a=input("wait key")
        return v 

# Compute BVH Roataion (Standard Algorithm)     


def compute_rotation(parent_pos, child_pos, special_case=False):
    # Sicherstellen, dass die Positionen 3D sind und als NumPy-Arrays vorliegen

    #print(parent_pos,child_pos)
    #a=input("wait key")
    

    parent_pos = np.array(parent_pos[0])
    child_pos = np.array(child_pos[1])

    #print(parent_pos,child_pos)
    #a=input("wait key")


    # Überprüfen, ob parent_pos und child_pos mehrere 3D-Punkte enthalten
    if parent_pos.shape[0] > 3:
        parent_pos = parent_pos[-1]  # Nimm den letzten Vektor, falls mehr als 3D-Positionen vorhanden sind

    if child_pos.shape[0] > 3:
        child_pos = child_pos[-1]  # Nimm den letzten Vektor, falls mehr als 3D-Positionen vorhanden sind

    # Überprüfen, ob parent_pos und child_pos die richtige Form haben (3D-Vektor)
    if parent_pos.shape != (3,) or child_pos.shape != (3,):
        print(f"Fehler: Ungültige Eingabe. Erwartet (3,), aber erhalten: Parent-Shape: {parent_pos.shape}, Child-Shape: {child_pos.shape}")
        return [0.0, 0.0, 0.0]

    # Berechne die Richtung des Kindes im Vergleich zum Elternteil
    direction = parent_pos - child_pos

    # Check if Zero Direction
    if (all(v == 0 for v in direction))==True:
         direction=[-0.0001,-0.0001,-0.0001]    
    

    #print(direction)
    #a=input("wait key")

    # Normiere die Richtung
    direction = normalize(direction)

    # Standard-Referenzachse (Y-Achse nach oben, Kinect: Z nach vorne)

    special_case=False
    if special_case:
        # Für spezielle Fälle wie Schultergelenke, bei denen wir die Z-Achse als Referenz nutzen
        ref_axis = np.array([0, 0, 1])  # Z-Achse als Referenz
    else:
        ref_axis = np.array([0, 1, 0])  # Standard Y-Achse als Referenz

    # Überprüfen, ob die Richtung (direction) der Referenzachse entspricht
    if np.allclose(direction, ref_axis):
        return [0.0, 0.0, 0.0]  # Keine Rotation nötig, wenn die Richtung übereinstimmt

    # Berechne die Rotation zwischen der Richtung und der Referenzachse
    # Hier übergeben wir beide Vektoren als 1D-Arrays (Shape (3,))
    rot, _ = R.align_vectors([direction], [ref_axis])  # Die Eingabe ist jetzt korrekt
    
    #print([direction],[ref_axis])
    #a=input("wait key")
    #rot, _  = R.align_vectors([direction], [ref_axis])


    # Wandle die Rotation in Euler-Winkel um
    euler = rot.as_euler('XYZ', degrees=True)  # Wandle Rotation in Euler-Winkel um

    # Optional: Transformation für Blender (Z-Achse nach oben, Y-Achse nach vorne)
    if not special_case:
        
        #euler[0], euler[1], euler[2] = euler[0], euler[2], euler[1]  # Tausche Z- und Y-Achse X-Achse
        
        #euler[0], euler[2] = euler[2], euler[0]  # Tausche x- und z-Achse
        euler[2], euler[1] = euler[1], euler[2]  # Tausche z- und y-Achse
        
        #euler[1], euler[2] = euler[2], euler[1]  # Tausche Z- und Y-Achse
        
        #euler[2] = -euler[2]  # Invertiere die Z-Achse (für Blender)
        pass
    return euler.tolist()




# Collect Rotaions at Frames

def collect_rotations(frame):
    rotations = {'Hip': [0.0, 0.0, 0.0]}  # Setze initiale Rotationen für das 'Hip'-Gelenk
    for parent, children in hierarchy.items():
        for child in children:
            #special_case = parent in ['ShoulderCenter', 'ShoulderLeft', 'ShoulderRight']
            special_case = parent in ['Hip']

            if parent in frame and child in frame:
                # Berechne die Rotation für das aktuelle Kind
                rot = compute_rotation(frame[parent], frame[child], special_case=special_case)
                
                # Optional: Anpassung der Rotation für Blender
                #rot = transform_rotation_for_blender(rot)
                
                rotations[parent] = rot
                
                # Debugging-Ausgabe
                #print(f"Rotation für {child} von {parent}: {rot}")

            else:
                # Falls ein Gelenk im Frame fehlt, setzen wir die Rotation auf [0.0, 0.0, 0.0]
                rotations[parent] = [0.0, 0.0, 0.0]
                #print(f"Fehler: {parent} oder {child} fehlen im Frame!")

    # Optional: Debugging-Ausgabe
    #print("Alle Rotationen: ", rotations)
    
    return rotations




# do not use, its not working correct

# Beispiel für die Umwandlung der Rotationen
def transform_rotation_for_blender(rot):
    # Blender erwartet Z-Achse nach oben, Kinect nach vorne
    rot = np.array(rot)

    # Tausche Z- und Y-Achse
    rot[0], rot[1] = rot[1], rot[0]  # Z -> Y und Y -> Z

    # Invertiere Z-Achse
    rot[2] = -rot[2]  # Negiere die Z-Achse
    
    # Rückgabe der angepassten Rotation
    return rot.tolist()




# BVH-Schreiberfunktionen

def write_joint(f, name, frame, parent_name=None, depth=0):
    indent = '\t' * depth
    is_root = name == 'Hip'

    if parent_name:
        # Hole die Positionen des Elternteils und des aktuellen Gelenks
        parent_pos = frame.get(parent_name, None)
        child_pos = frame.get(name, None)

        # Fehlerbehandlung: Wenn Positionen fehlen oder ungültig sind, Standardwert verwenden
        if parent_pos is None or child_pos is None:
            #print(f"Fehler: Positionen fehlen für {name} (parent: {parent_name}). Parent: {parent_pos}, Child: {child_pos}")
            offset = np.array([0.0, 0.0, 0.0])  # Rückgabe eines Standardwertes
        else:
            # Debugging: Ausgabe der extrahierten Positionen
            #print(f"Name: {name}, Parent Name: {parent_name}")
            #print(f"Parent Position (vor der Korrektur): {parent_pos}")
            #print(f"Child Position (vor der Korrektur): {child_pos}")

            # Wenn parent_pos und child_pos jeweils zwei Positionen haben, verwenden wir die letzte Position
            if isinstance(parent_pos, (tuple, list)) and len(parent_pos) == 2:
                parent_pos = parent_pos[-1]
            
            if isinstance(child_pos, (tuple, list)) and len(child_pos) == 2:
                child_pos = child_pos[-1]

            # Debugging: Ausgabe der korrigierten Positionen
            #print(f"Parent Position (nach der Korrektur): {parent_pos}")
            #print(f"Child Position (nach der Korrektur): {child_pos}")

            # Berechne den Offset
            offset = compute_offset(parent_pos, child_pos, name)
            #print(f"Berechneter Offset für {name}: {offset}")

    else:
        # Wenn kein Elternteil (root-Gelenk), setze den Offset auf Null
        offset = np.array([0.0, 0.0, 0.0])

    joint_type = "ROOT" if is_root else "JOINT"

    # Schreibe das Gelenk in die BVH-Datei
    f.write(f"{indent}{joint_type} {name}\n")
    f.write(f"{indent}{{\n")
    f.write(f"{indent}\tOFFSET {offset[0]:.2f} {offset[1]:.2f} {offset[2]:.2f}\n")
    
    # Wurzelgelenk (Hip) bekommt 6 Kanäle (Position und Rotation), alle anderen nur 3 (Rotation)
    if is_root:
        f.write(f"{indent}\tCHANNELS 6 Xposition Yposition Zposition Xrotation Yrotation Zrotation\n")
    else:
        f.write(f"{indent}\tCHANNELS 3 Xrotation Yrotation Zrotation\n")

    # Rekursive Verarbeitung der Kindgelenke
    for child in hierarchy.get(name, []):
        write_joint(f, child, frame, name, depth + 1)

    if name not in hierarchy:
        f.write(f"{indent}\tEnd Site\n")
        f.write(f"{indent}\t{{\n")
        f.write(f"{indent}\t\tOFFSET 0.0 0.0 0.0\n")
        f.write(f"{indent}\t}}\n")

    f.write(f"{indent}}}\n")


# Compute Offset in BVH File

def compute_offset(parent_pos, child_pos, name):
    # Sicherstellen, dass die Eingabepositionen 3D sind
    if isinstance(parent_pos, (tuple, list)) and len(parent_pos) == 3:
        parent_pos = np.array(parent_pos)
    else:
        print(f"Fehler: Ungültige Elternposition für {name}: {parent_pos}")
        parent_pos = np.array([0.0, 0.0, 0.0])

    if isinstance(child_pos, (tuple, list)) and len(child_pos) == 3:
        child_pos = np.array(child_pos)
    else:
        print(f"Fehler: Ungültige Kindposition für {name}: {child_pos}")
        child_pos = np.array([0.0, 0.0, 0.0])

    # Berechne den Offset zwischen den Positionen des Eltern- und Kindgelenks
    offset = child_pos - parent_pos

    # Debugging-Ausgabe
    #print(f"Berechneter Offset für {name}: Parent Position: {parent_pos}, Child Position: {child_pos}, Offset: {offset}")
    #a=input("wait key")
    return offset



# BVH schreiben

def write_bvh(frames, filename="output.bvh"):
    with open(filename, 'w') as f:
        f.write("HIERARCHY\n")
        write_joint(f, "Hip", frames[0])  # Schreibe die Hierarchie

        f.write("MOTION\n")
        f.write(f"Frames: {len(frames)}\n")
        f.write("Frame Time: 0.1\n")  # Standard Framezeit

        for frame in frames:
            rotations = collect_rotations(frame)  # Berechne Rotationen für das aktuelle Frame
            root_pos = frame["Hip"][0]  # Parent Position
            
            root_rot = rotations["Hip"]

            # Füge globale Korrekturrotation hinzu
            r_original = R.from_euler('XYZ', root_rot, degrees=True)

            # Weltrotation: Z -45°, Y -45° → korrekte Ausrichtung
            z_fix = R.from_euler('Z', 0, degrees=True)
            y_fix = R.from_euler('Y', 0, degrees=True)
            x_fix = R.from_euler('X', 45, degrees=True)

            correction = x_fix * y_fix * z_fix

            r_corrected = correction * r_original
            root_rot = r_corrected.as_euler('XYZ', degrees=True).tolist()


            #root_rot = rotations["Hip"]

            data = [*root_pos, *root_rot]

            def write_joint_motion(name):
                if name == "Hip":
                    pass  # Wurzelgelenk wird bereits verarbeitet
                else:
                    rot = rotations.get(name, [0.0, 0.0, 0.0])
                    data.extend(rot)
                for child in hierarchy.get(name, []):
                    write_joint_motion(child)

            write_joint_motion("Hip")
            f.write(" ".join(f"{v:.2f}" for v in data) + "\n")
    
    print("")
    print("")
    print(f"BVH file written to {filename}")
    print("")



# Hauptfunktion

if __name__ == "__main__":

    # Init Message

    os.system("cls")

    print("")
    print("")
    print("Hermanns Blender-Compatible BVH Exporter")
    print("")
    print("use Kinect_Writer for .txt export")
    print("")
    path = input("Path to RAW Kinect TXT file: ").strip('"')
    print("")
    print("")
   

    # Check Path

    if not os.path.exists(path):
        print("File not found.")
        exit(1)

    # read Frames from Kinect RAW .txt File       

    print("Importing Frames...")
    print("")

    frames = read_frames_from_file(path)
    if len(frames) == 0:
        print("Fehler: Keine gültigen Frames gefunden! Prüfe die Eingabedatei.")
        a=input("wait key")
        exit(1)

    # Get Output Path

    dir_path = os.path.dirname(os.path.realpath(__file__))
    now = datetime.now()
    output_file = dir_path + f"/motion_{now.strftime('%Y%m%d_%H%M%S')}.bvh"  # Dateiname mit Zeitstempel

    # Write BVH

    print("Writing BVH File please wait...")
    print("")

    write_bvh(frames, output_file)

    # Finished
   
    print("")
    print("Finished...")
    
    print("")
    input("Press any key to exit.")
    exit()
