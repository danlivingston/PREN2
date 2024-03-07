import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import time
import pygetwindow as gw
import pyautogui

# JSON-Daten einlesen
with open("config03.json", "r") as file:
    data = json.load(file)
config = data["config"]

# Farbkodierung anpassen, leere Einträge als vollständig transparent interpretieren
color_mapping = {
    "red": (1, 0, 0, 1),
    "blue": (0, 0, 1, 1),
    "yellow": (1, 1, 0, 1),
    "": (0, 0, 0, 0),  # Transparent für leere Einträge
}
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
    (-spacing / 2, spacing / 2, spacing / 2),
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
    ax.bar3d(
        pos[0], pos[1], pos[2], cube_size, cube_size, cube_size, color=color, shade=True
    )

def update(frame):
    draw_cube(cube_positions[frame], colors[frame])

ani = FuncAnimation(
    fig, update, frames=len(cube_positions), interval=1000, repeat=False
)

plt.show()

# Fensterbewegung nach Anzeige
time.sleep(1)  # Warten, damit das Fenster Zeit hat, erstellt zu werden

# Bildschirmauflösung ermitteln
screen_width, screen_height = pyautogui.size()

try:
    # Annahme: Der Fenstertitel ist "Figure 1"
    windows = gw.getWindowsWithTitle("Figure 1")
    if windows:
        window = windows[0]
        # Berechnen der neuen Position: Rechts auf dem Hauptbildschirm
        # Diese Koordinaten könnten das Fenster auf den rechten Monitor verschieben, wenn Sie mehr als einen Monitor haben
        new_x_position = screen_width - window.width - 20  # Etwas Abstand vom rechten Rand
        window.moveTo(new_x_position, 100)  # Bewegen Sie das Fenster nach rechts
except IndexError:
    print("Fenster nicht gefunden. Stellen Sie sicher, dass der Fenstertitel korrekt ist.")
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
