import psutil
import time

while True:
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    print(f"CPU Usage: {cpu_usage}%")
    print(f"RAM Usage: {ram_usage}%")
    print(f"Disk Usage: {disk_usage}%")

    time.sleep(3)  # Aktualisiert alle 5 Sekunden
