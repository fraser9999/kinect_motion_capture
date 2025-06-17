#Kinect Anim Plotter
#Hermann Knopp
#2025
#python 3.10.10

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Funktion zum Lesen der 3D-Daten aus einer Datei
def read_3d_data_from_file(file_path):
    frames = []
    current_frame = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "":  # Leerzeile signalisiert das Ende eines Frames
                if current_frame:
                    frames.append(current_frame)
                    current_frame = []
            else:
                parts = line.split()
                # Extrahiere die 3D-Koordinaten (wir ignorieren den Namen)
                try:
                    x1, y1, z1 = map(float, parts[1:4])
                    x2, y2, z2 = map(float, parts[4:])
                    current_frame.append(((x1, y1, z1), (x2, y2, z2)))
                except ValueError:
                    print(f"Skipping invalid line: {line}")
                    continue
        
        # Füge das letzte Frame hinzu, falls es nicht mit einer Leerzeile endet
        if current_frame:
            frames.append(current_frame)
    
    return frames

# Funktion zum Plotten der 3D-Linien und zur Erstellung der Animation
def plot_3d_animation(frames):
    # Erstelle die Figur und das 3D-Achsen-Objekt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Initialisiere die Linien, basierend auf der Anzahl der Linien im ersten Frame
    lines = [ax.plot([], [], [], marker='o', linestyle='-', color='b')[0] for _ in range(len(frames[0]))]

    # Achsenbeschriftungen
    ax.set_xlabel('X-Achse')
    ax.set_ylabel('Y-Achse')
    ax.set_zlabel('Z-Achse')
    ax.set_title('3D Linienanimation')

    # Setze die Grenzen der Achsen dynamisch, basierend auf den Daten
    def set_dynamic_limits():
        # Holen Sie sich alle x, y, z Werte aus allen Frames
        x_vals = []
        y_vals = []
        z_vals = []

        for frame in frames:
            for ((x1, y1, z1), (x2, y2, z2)) in frame:
                x_vals.extend([x1, x2])
                y_vals.extend([y1, y2])
                z_vals.extend([z1, z2])

        ax.set_xlim(min(x_vals) - 1, max(x_vals) + 1)
        ax.set_ylim(min(y_vals) - 1, max(y_vals) + 1)
        ax.set_zlim(min(z_vals) - 1, max(z_vals) + 1)

    # Funktionsaufruf zum Initialisieren der Animation
    def init():
        print("Initializing lines...")
        for line in lines:
            line.set_data([], [])  # Setzt die Linien mit leeren Daten für den Start
            line.set_3d_properties([])  # Leere 3D-Koordinaten für den Start
        set_dynamic_limits()  # Dynamische Achsenlimits setzen
        return lines

    # Funktionsaufruf zum Aktualisieren der Daten bei jedem Frame
    def update(frame):
        print(f"Updating frame {frames.index(frame)}...")
        # Prüfe, ob das aktuelle Frame die richtige Anzahl von Linien enthält
        if len(frame) != len(lines):
            print(f"Skipping frame with {len(frame)} lines (expected {len(lines)}).")
            return lines
        
        # Aktualisiere jede Linie mit den neuen 3D-Koordinaten
        for i, (line, ((x1, y1, z1), (x2, y2, z2))) in enumerate(zip(lines, frame)):
            # Stelle sicher, dass alle Koordinaten gültig sind
            if any(np.isnan(coord) for coord in [x1, y1, z1, x2, y2, z2]):
                print(f"Skipping line with invalid coordinates: {x1}, {y1}, {z1}, {x2}, {y2}, {z2}")
                continue

            # Aktualisiere die Linie mit den neuen 3D-Koordinaten
            line.set_data([x1, x2], [y1, y2])
            line.set_3d_properties([z1, z2])

        return lines

    # Erstelle die Animation
    ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=20, repeat=True)

    plt.show()

def main():
    os.system("cls")
    print("")
    print("3D Animation Renderer for Kinect Test Data")
    print("")

    file_path = input("Path to Kinect 3D Frame (.txt): ").strip('"')
    if not file_path:
        print("No File found...")
        input("Press any key to exit.")
        exit()

    # Lese die Frames aus der Datei
    frames = read_3d_data_from_file(file_path)
    
    # Überprüfe, ob Frames vorhanden sind
    if len(frames) == 0:
        print("No data found in the file.")
        input("Press any key to exit.")
        exit()

    # Zeige die Animation der 3D-Daten an
    plot_3d_animation(frames)

if __name__ == "__main__":
    main()
