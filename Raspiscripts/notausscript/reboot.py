import subprocess


def restart_raspberry_pi():
    try:
        # Führt den Neustart-Befehl aus
        subprocess.run(["sudo", "reboot"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Neustart: {e}")


if __name__ == "__main__":
    restart_raspberry_pi()
