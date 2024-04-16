import smbus2
import tkinter as tk
from threading import Thread
import time
import os
from datetime import datetime

# Pfadkonfiguration
base_dir = os.path.dirname(os.path.abspath(__file__))
SIGNAL_FILE_PATH = os.path.join(base_dir, 'signal.txt')

# Konstanten für den PAC1934
I2C_ADDR = 0x10
REG_VOLTAGE = 0x07
REG_CURRENT = 0x13
REG_POWER = 0x17
REG_POWER_ACC = 0x03
REG_ACC_COUNT = 0x02
REFRESH_COMMAND = 0x00
REFRESH_V_COMMAND = 0x1F
CTRL_REGISTER_ADDR = 0x01
CHDIS_REGISTER_ADDR = 0x1C
NEGPWR_REGISTER_ADDR = 0x1D
CONFIG_BYTE = 0x00
SAMPLE_RATE = 0b11
FSV = 32.0
FSC = 25.0
POWER_FSR = 800
R_SENSE = 0.004
DENOMINATOR = 0xFFFF
T_clock = 1024

class MockSMBus:
    def write_byte(self, addr, value):
        print(f"Mock write_byte to addr {addr} with value {value}")
    def write_byte_data(self, addr, reg, value):
        print(f"Mock write_byte_data to addr {addr}, reg {reg} with value {value}")
    def read_i2c_block_data(self, addr, reg, length):
        import random
        return [random.randint(0, 255) for _ in range(length)]

try:
    bus = smbus2.SMBus(1)
except FileNotFoundError:
    bus = MockSMBus()

start_time = datetime.now()
accumulated_energy = 0

def clear_signal_file():
    with open(SIGNAL_FILE_PATH, 'w') as file:
        file.truncate()  # Clears the file at the beginning

def send_refresh_v_command():
    bus.write_byte(I2C_ADDR, REFRESH_V_COMMAND)

def read_voltage():
    raw_voltage = bus.read_i2c_block_data(I2C_ADDR, REG_VOLTAGE, 2)
    voltage = FSV * ((raw_voltage[0] << 8) | raw_voltage[1]) / DENOMINATOR
    return round(voltage, 2)

def read_current():
    raw_current = bus.read_i2c_block_data(I2C_ADDR, REG_CURRENT, 2)
    current = FSC * ((raw_current[0] << 8) | raw_current[1]) / DENOMINATOR
    return round(current, 3)

def read_power():
    raw_power = bus.read_i2c_block_data(I2C_ADDR, REG_POWER, 4)
    power = POWER_FSR * ((raw_power[0] << 24) | (raw_power[1] << 16) | (raw_power[2] << 8) | raw_power[3]) / 268435455
    return round(power, 2)

def read_energy():
    raw_energy = bus.read_i2c_block_data(I2C_ADDR, REG_POWER_ACC, 6)
    energy = (int.from_bytes(raw_energy, byteorder='big') / 268435455) * POWER_FSR * T_clock / 3600000  # Convert to Wh
    return round(energy, 3)

def check_signal():
    try:
        with open(SIGNAL_FILE_PATH, 'r') as file:
            signal = file.read().strip()
            return signal == 'stop'
    except FileNotFoundError:
        return False

def main_monitoring():
    clear_signal_file()
    global accumulated_energy
    while True:
        send_refresh_v_command()
        time.sleep(0.005)
        voltage = read_voltage()
        current = read_current()
        power = read_power()
        energy = read_energy()
        accumulated_energy += energy
        time.sleep(0.1)
        if check_signal():
            show_results()
            break

def show_results():
    elapsed_time = datetime.now() - start_time
    elapsed_seconds = int(elapsed_time.total_seconds())  # Gesamtsekunden seit Start

    root = tk.Tk()
    root.title("Energiemessung Ergebnisse")

    # Fenstergröße und Position
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.52)  # 52% der Bildschirmbreite
    window_height = screen_height  # Ganze Bildschirmhöhe verwenden
    x_coordinate = 0  # Startet am linken Bildschirmrand
    y_coordinate = 0  # Startet am oberen Bildschirmrand

    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    
    # Frame für zentrierte Inhalte
    frame = tk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH)

    # Label für Laufzeit, das auch die Sekunden in Kurzform anzeigt
    label_time = tk.Label(frame, text=f"Laufzeit: {elapsed_time} ({elapsed_seconds}s)", font=('Helvetica', 50), bg='white')
    label_time.pack(expand=True)
    label_energy = tk.Label(frame, text=f"Verbrauchte Energie: {accumulated_energy:.3f} Wh", font=('Helvetica', 40), bg='white')
    label_energy.pack(expand=True)

    root.after(10000, root.destroy)  # Schließt das Fenster nach 10 Sekunden
    root.mainloop()
    os._exit(0)

if __name__ == '__main__':
    main_monitoring()
