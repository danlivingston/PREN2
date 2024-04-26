import smbus2
import tkinter as tk
from threading import Thread
import time
import os
from datetime import datetime

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

def send_refresh_command():
    bus.write_byte(I2C_ADDR, REFRESH_COMMAND)

def send_refresh_v_command():
    bus.write_byte(I2C_ADDR, REFRESH_V_COMMAND)

def send_ctrlreg_command():
    CONFIG_BYTE = 0x80
    bus.write_byte_data(I2C_ADDR, CTRL_REGISTER_ADDR, CONFIG_BYTE)

def send_chdis_command():
    SET_BYTE = 0x70
    bus.write_byte_data(I2C_ADDR, CHDIS_REGISTER_ADDR, SET_BYTE)

def send_negpwr_command():
    SET_BYTE = 0x0
    bus.write_byte_data(I2C_ADDR, NEGPWR_REGISTER_ADDR, SET_BYTE)

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
    calc_power = (raw_power[0] << 24) | (raw_power[1] << 16) | (raw_power[2] << 8) | raw_power[3]
    power = POWER_FSR * calc_power / 268435455
    return round(power, 2)

def read_energy():
    raw_energy = bus.read_i2c_block_data(I2C_ADDR, REG_POWER_ACC, 6)
    acc_count = bus.read_i2c_block_data(I2C_ADDR, REG_ACC_COUNT, 3)
    int_energy = int.from_bytes(raw_energy, byteorder='big')
    int_count = int.from_bytes(acc_count, byteorder='big')
    energy = (((int_energy / 268435455) * POWER_FSR) * (1 / 1024)) * 100 * 1.25
    return round(energy, 8)

def update_display():
    while True:
        send_refresh_v_command()
        time.sleep(0.005)
        voltage = read_voltage()
        current = read_current()
        power = read_power()
        energy = read_energy()
        voltage_label.config(text=f"Spannung: {voltage} V")
        current_label.config(text=f"Strom: {current} A")
        power_label.config(text=f"Leistung: {power} W")
        energy_label.config(text=f"Energie: {energy} Ws")
        time.sleep(0.1)

root = tk.Tk()
root.title("Energiemessung")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width//2}x{screen_height//2}+0+0")

voltage_label = tk.Label(root, text="Spannung: ", font=('Helvetica', 16))
voltage_label.pack()
current_label = tk.Label(root, text="Strom: ", font=('Helvetica', 16))
current_label.pack()
power_label = tk.Label(root, text="Leistung: ", font=('Helvetica', 16))
power_label.pack()
energy_label = tk.Label(root, text="Energie: ", font=('Helvetica', 16))
energy_label.pack()

thread = Thread(target=update_display)
thread.daemon = True
thread.start()

root.mainloop()
