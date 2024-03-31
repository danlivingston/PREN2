import subprocess

def kill_all_python_processes():
    try:
        # Beendet alle Prozesse, die in ihrem Namen "python" enthalten
        subprocess.run(["pkill", "-f", "python"], check=True)
        print("Alle Python-Prozesse wurden erfolgreich beendet.")
    except subprocess.CalledProcessError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

kill_all_python_processes()
