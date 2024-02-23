import os
import signal
import subprocess

# Befehl ausführen, um alle laufenden Python 3-Prozesse zu finden
try:
    prozesse = subprocess.check_output(["pgrep", "-f", "python3"]).decode('utf-8')
except subprocess.CalledProcessError:
    # Kein Prozess gefunden
    prozesse = ""

# Jeden gefundenen Prozess beenden
for pid in prozesse.splitlines():
    print(f"Beende Python 3-Prozess mit PID {pid}")
    os.kill(int(pid), signal.SIGTERM)  # SIGTERM senden, um den Prozess zu beenden
