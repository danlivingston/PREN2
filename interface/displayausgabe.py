import json
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D, art3d
from matplotlib.animation import FuncAnimation

# JSON-Daten einlesen
with open('config03.json', 'r') as file:
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

plt.show()
