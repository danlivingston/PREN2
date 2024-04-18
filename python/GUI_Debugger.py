import tkinter as tk
from tkinter import ttk
import Funktionen  # Importiere das modifizierte Funktionen.py Skript

root = tk.Tk()
root.title("Talis Visual Debugger")
root.geometry("600x600")

# Stildefinitionen
buttonStyle = {"font": ("Helvetica", 12), "bg": "#D5D8DC", "fg": "black"}
entryStyle = {"font": ("Helvetica", 12), "relief": tk.FLAT}

# Haupt-Frame, der alle Widgets enthält
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Begrüßungstext
label = tk.Label(main_frame, text="Willkommen zum Visual Debugger, have fun testing!", font=("Helvetica", 14))
label.pack(pady=(0,20))

# Frame für Stössel-Buttons
stossel_frame = ttk.Frame(main_frame)
stossel_frame.pack(pady=(0,10))

# Einzeln Stössel steuern
for i in range(1, 5):
    button = tk.Button(stossel_frame, text=f"Stössel {i} ansteuern", cursor="hand2", **buttonStyle, command=lambda i=i: Funktionen.stossel_ansteuern(i))
    button.pack(side=tk.LEFT, padx=5, pady=2)

# Frame für Steppermotor-Steuerung
motor_frame = ttk.Frame(main_frame)
motor_frame.pack(pady=(0,10), fill=tk.X)


# Eingabefeld und Button für den Steppermotor
eingabefeld_steps = tk.Entry(motor_frame, **entryStyle)
eingabefeld_steps.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,5))
tk.Button(motor_frame, text="Motor Steps Ausführen", command=lambda: Funktionen.motor_steps(int(eingabefeld_steps.get())), **buttonStyle).pack(side=tk.LEFT, padx=(5,0))


# Eingabefeld für Delay-Einstellungen
delay_frame = ttk.Frame(main_frame)
delay_frame.pack(pady=(10, 20), fill=tk.X)
delay_label = tk.Label(delay_frame, text="Delay einstellen (s):", font=("Helvetica", 12))
delay_label.pack(side=tk.LEFT)
eingabefeld_delay = tk.Entry(delay_frame, **entryStyle)
eingabefeld_delay.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 20))

# Buttons für Drehung um 90 und 30 Grad
drehung_frame = ttk.Frame(main_frame)
drehung_frame.pack(pady=(0,10))
tk.Button(drehung_frame, text="90° drehen", command=lambda: Funktionen.drehen_um_grad(90), **buttonStyle).pack(side=tk.LEFT, padx=(5,0))
tk.Button(drehung_frame, text="30° drehen", command=lambda: Funktionen.drehen_um_grad(30), **buttonStyle).pack(side=tk.LEFT, padx=(5,0))

# Button für Motorbremse
#tk.Button(main_frame, text="Motorbremse umschalten", command=Funktionen.motor_bremse, **buttonStyle).pack(pady=5)

# Button für einen kompletten Durchlauf
tk.Button(main_frame, text="Kompletter Durchlauf", command=Funktionen.kompletter_durchlauf, **buttonStyle).pack(pady=5)

# Notaus-Knopf
tk.Button(main_frame, text="NOTAUS", command=Funktionen.notaus, bg="#FF0000", fg="white", font=("Helvetica", 12)).pack(pady=(5,0))

# Stop Button für den Steppermotor
tk.Button(main_frame, text="Motor Stop", command=Funktionen.motor_stop, bg="#E74C3C", fg="white", font=("Helvetica", 12)).pack(pady=(5,0))

root.mainloop()
