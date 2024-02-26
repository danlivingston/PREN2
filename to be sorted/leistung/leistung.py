import time

import psutil

while True:
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent

    print(f"{time.asctime()}")
    print(f"CPU Usage: {cpu_usage}%")
    print(f"RAM Usage: {ram_usage}%")
    print(f"Disk Usage: {disk_usage}%")
    time.sleep(1)
    print(f"\033[F\033[A\033[A\033[A\033[A")
