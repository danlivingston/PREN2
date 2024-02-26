import json

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D, art3d

# JSON-Daten einlesen
with open("config01.json", "r") as file:
    data = json.load(file)
config = data["config"]

# Farbkodierung anpassen, leere Einträge als 'grey' (Grau) interpretieren
color_mapping = {"red": "r", "blue": "b", "yellow": "y", "": "grey"}
colors = [color_mapping.get(config[str(i)], "grey") for i in range(1, 9)]

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
    (-spacing / 2, spacing / 2, spacing / 2),
]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Ansicht anpassen
elev = 20  # Vertikale Ausrichtung
azim = -128  # Horizontale Drehung
ax.view_init(elev=elev, azim=azim)

ax.set_xlim([-50, 50])
ax.set_ylim([-50, 50])
ax.set_zlim([-50, 50])
ax.set_axis_off()


def draw_cube(pos, color):
    ax.bar3d(
        pos[0], pos[1], pos[2], cube_size, cube_size, cube_size, color=color, shade=True
    )


def update(frame):
    draw_cube(cube_positions[frame], colors[frame])


ani = FuncAnimation(
    fig, update, frames=len(cube_positions), interval=1000, repeat=False
)

plt.show()
