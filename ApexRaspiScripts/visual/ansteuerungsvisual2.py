import tkinter as tk

def toggle_visibility():
    """Wechselt die Sichtbarkeit des Nachrichtenlabels."""
    if label.winfo_ismapped():
        label.pack_forget()  # Versteckt das Label, wenn es sichtbar ist
    else:
        label.pack(fill='both', expand=True)  # Zeigt das Label, wenn es versteckt ist
    root.after(500, toggle_visibility)  # Ruft die Funktion alle 500ms auf

def start_blinking_message():
    """Startet die blinkende Nachricht."""
    toggle_visibility()  # Startet das Blinken

def create_gui():
    """Erstellt das GUI-Fenster."""
    global root, label
    root = tk.Tk()
    root.title("Würfel Status")

    # Einstellen der Fenstergröße und -position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.52)  # 52der Bildschirmbreite
    window_height = screen_height
    x_position = 0
    y_position = 0
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Erstellen eines Labels für die Nachricht
    label = tk.Label(root, text="Auswurfmechanismus in Bearbeitung", font=("Arial", 40), fg="green")

    start_blinking_message()  # Startet das Blinken der Nachricht

    root.mainloop()

create_gui()
