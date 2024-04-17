import json
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D, art3d
from matplotlib.animation import FuncAnimation
import os
import threading
import time

# Basisverzeichnis relativ zum aktuellen Skript ermitteln
base_dir = os.path.dirname(os.path.abspath(__file__))

# Pfad zur JSON-Datei im "videos"-Ordner
json_file_path = os.path.join(base_dir, 'videos', 'config03.json')

# JSON-Daten einlesen
with open(json_file_path, 'r') as file:
    data = json.load(file)
config = data['config']

# Farbkodierung anpassen, leere Einträge als vollständig transparent interpretieren
color_mapping = {'red': (1, 0, 0, 1), 'blue': (0, 0, 1, 1), 'yellow': (1, 1, 0, 1), '': (0, 0, 0, 0)}
colors = [color_mapping.get(config[str(i)], (0, 0, 0, 0)) for i in range(1, 9)]

# Würfelkantenlänge und Positionen
cube_size = 20
spacing = 22
cube_positions = [
    (-spacing / 2, -spacing / 2, -spacing / 2),
    (spacing / 2, -spacing / 2, -spacing / 2),
    (spacing / 2, spacing / 2, -spacing / 2),
    (-spacing / 2, spacing / 2, -spacing / 2),
    (-spacing / 2, -spacing / 2, spacing / 2),
    (spacing / 2, -spacing / 2, spacing / 2),
    (spacing / 2, spacing / 2, spacing / 2),
    (-spacing / 2, spacing / 2, spacing / 2)
]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Ansicht anpassen
elev = 20  # Vertikale Ausrichtung
azim = -128  # Horizontale Drehung
ax.view_init(elev=elev, azim=azim)

ax.set_xlim([-50, 50])
ax.set_ylim([-50, 50])
ax.set_zlim([-50, 50])
ax.set_axis_off()

def draw_cube(pos, color):
    ax.bar3d(pos[0], pos[1], pos[2], cube_size, cube_size, cube_size, color=color, shade=True)

def update(frame):
    draw_cube(cube_positions[frame], colors[frame])

ani = FuncAnimation(fig, update, frames=len(cube_positions), interval=1000, repeat=False)

# Funktion, die das Fenster nach einer bestimmten Zeit schließt
def close_figure_after_delay(delay):
    time.sleep(delay)  # Warten
    plt.close(fig)  # Fenster schließen

# Thread starten, der das Fenster nach der Dauer der Animation plus 3 Sekunden schließt
threading.Thread(target=close_figure_after_delay, args=(len(cube_positions) * 1 + 3,)).start()

plt.show()
