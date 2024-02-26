import json

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D, art3d

# JSON-Daten einlesen
with open("config03.json", "r") as file:
    data = json.load(file)
config = data["config"]

# Farbkodierung anpassen, leere Einträge als vollständig transparent interpretieren
color_mapping = {
    "red": (1, 0, 0, 1),
    "blue": (0, 0, 1, 1),
    "yellow": (1, 1, 0, 1),
    "": (0, 0, 0, 0),
}
colors = [color_mapping.get(config[str(i)], (0, 0, 0, 0)) for i in range(1, 9)]

# Würfelkantenlänge, Positionen und Geschwindigkeit des Fallens
cube_size = 20
spacing = 22
start_height = 100
falling_speed = 5  # Geschwindigkeit des Fallens

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
ax.set_zlim([-start_height, 50])
ax.set_axis_off()


def draw_cube(pos, color, z_pos):
    ax.bar3d(
        pos[0], pos[1], z_pos, cube_size, cube_size, cube_size, color=color, shade=True
    )


def update(frame):
    ax.cla()
    ax.set_axis_off()
    ax.set_xlim([-50, 50])
    ax.set_ylim([-50, 50])
    ax.set_zlim([-start_height, 50])
    ax.view_init(elev=elev, azim=azim)

    # Zeige nur Würfel, die fallen oder bereits gefallen sind
    for i in range(len(cube_positions)):
        if frame >= i * 10:
            z_pos = max(
                cube_positions[i][2] - falling_speed * (frame - i * 10),
                cube_positions[i][2],
            )
            draw_cube(cube_positions[i], colors[i], z_pos)


ani = FuncAnimation(
    fig, update, frames=10 * len(cube_positions), interval=50, repeat=False
)

plt.show()
