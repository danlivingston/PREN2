import tkinter as tk
import psutil
import time

def update_stats():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    net_io = psutil.net_io_counters()
    uptime = time.time() - psutil.boot_time()

    # Konvertierung der Uptime in Stunden, Minuten und Sekunden
    uptime_hours, uptime_remainder = divmod(uptime, 3600)
    uptime_minutes, uptime_seconds = divmod(uptime_remainder, 60)

    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    ram_label.config(text=f"RAM Usage: {ram_usage}%")
    disk_label.config(text=f"Disk Usage: {disk_usage}%")
    net_label.config(text=f"Net Sent: {net_io.bytes_sent} bytes, Net Received: {net_io.bytes_recv} bytes")
    uptime_label.config(text=f"System Uptime: {int(uptime_hours)}h {int(uptime_minutes)}m {int(uptime_seconds)}s")

    window.after(1000, update_stats)

# Fenster erstellen
window = tk.Tk()
window.title("Systemüberwachung")

# Labels erstellen
cpu_label = tk.Label(window, text="CPU Usage: ", font=("Helvetica", 12))
cpu_label.pack()

ram_label = tk.Label(window, text="RAM Usage: ", font=("Helvetica", 12))
ram_label.pack()

disk_label = tk.Label(window, text="Disk Usage: ", font=("Helvetica", 12))
disk_label.pack()

net_label = tk.Label(window, text="Network Usage: ", font=("Helvetica", 12))
net_label.pack()

uptime_label = tk.Label(window, text="System Uptime: ", font=("Helvetica", 12))
uptime_label.pack()

# Statistiken initial aktualisieren
update_stats()

# GUI-Schleife starten
window.mainloop()
