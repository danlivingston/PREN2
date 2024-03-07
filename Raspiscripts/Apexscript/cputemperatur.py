import platform
import psutil
import subprocess

def get_cpu_temperature():
    """
    Function to retrieve the CPU temperature in Celsius, handling potential OS and library compatibility issues.

    Raises:
        RuntimeError: If the operating system is not supported or a necessary library is missing.
        psutil.NoSuchSensor: If the CPU temperature sensor cannot be found on the system.

    Returns:
        float: The CPU temperature in Celsius, if successful.
    """

    if platform.system() == "Darwin":
        # macOS
        try:
            return psutil.sensors_temperatures()['cpu'][0].current
        except psutil.NoSuchSensor:
            raise RuntimeError("CPU temperature sensor unavailable on macOS.")
    elif platform.system() == "Linux":
        # Raspberry Pi or other Linux systems
        try:
            output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
            return float(output.split("=")[1].split("'")[0])
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Handle potential system-specific issues on Linux
            raise RuntimeError("Error retrieving CPU temperature on Linux.")
    else:
        raise RuntimeError(f"Operating system '{platform.system()}' not supported.")

while True:
    try:
        # CPU-Temperatur abrufen
        cpu_temperatur = get_cpu_temperature()

        # Ausgabe der Temperatur
        print(f"CPU-Temperatur: {cpu_temperatur:.1f} °C")

    except (RuntimeError, psutil.NoSuchSensor) as e:
        print(f"Error: {e}")

    # 1 Sekunde warten
    time.sleep(1)
