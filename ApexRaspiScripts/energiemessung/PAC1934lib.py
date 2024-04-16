import smbus2
import tkinter as tk
from threading import Thread
import time

# Konstanten für den PAC1934
I2C_ADDR = 0x10   #Standard I2C-Adresse des PAC1934
REG_VOLTAGE = 0x07  # Registeradresse für Spannungsmessung
REG_CURRENT = 0x13  # Registeradresse für Strommessung
REG_POWER = 0x17    # Registeradresse für Leistung Vsense x Vbus
REG_POWER_ACC = 0x03 # Registeradresse für akkumulierte Leistung
REG_ACC_COUNT = 0x02    #REgisteradresse für akku Count
REFRESH_COMMAND = 0x00 #Registeradresse für Refreshbefehl
REFRESH_V_COMMAND = 0x1F #Registeradresse für Refresh V, Akkumulatoren werden NICHT zurückgesetzt
CTRL_REGISTER_ADDR = 0x01 #Registeradresse vom Controlregister
CHDIS_REGISTER_ADDR = 0x1C # Registeradresse für Kanal Ein Ausschalten
NEGPWR_REGISTER_ADDR = 0x1D #Registeradresse um Messung Bidirektional zu machen
CONFIG_BYTE = 0x00 #Konfigurations Byte für Controlregister
# Konstanten für Konfiguration
SAMPLE_RATE = 0b00 #0b00 1024, 0b01 256, 0b10 64, 0b11 8 samples/s

# Konstanten für Berechnung
FSV = 32.0  # Vollskalenspannung (32V)
FSC = 25.0  # Vollskalenstrom 
POWER_FSR = 800 #Vollskalenleistung
R_SENSE = 0.004  # RSENSE-Widerstandswert in Ohm
DENOMINATOR = 0xFFFF  # Fester Nennerwert für die Umrechnung
T_clock = 1024 # 100kHz

# SMBus Instanz erstellen
bus = smbus2.SMBus(1)


def send_refresh_command():
    #Sendet den Command um Messdaten register zu refreshen, vor jeder messung nötig
    bus.write_byte(I2C_ADDR, REFRESH_COMMAND)
    
def send_refresh_v_command():
    #Sendet den Command um Messdaten register zu refreshen, ohne akkumulatoren
    bus.write_byte(I2C_ADDR, REFRESH_V_COMMAND)

def send_ctrlreg_command():
    #ändert das controll register
    CONFIG_BYTE = 0x80#0b10000000
    bus.write_byte_data(I2C_ADDR, CTRL_REGISTER_ADDR, CONFIG_BYTE)
    
def send_chdis_command():
    #Kanäle ein und ausschalten
    SET_BYTE = 0x70 #0b01110000 #Schaltet Kanäle 2,3,4 inaktiv
    bus.write_byte_data(I2C_ADDR, CHDIS_REGISTER_ADDR, SET_BYTE)
    
def send_negpwr_command():
    #Bidirektionale messung einschalten
    SET_BYTE = 0x0
    bus.write_byte_data(I2C_ADDR, NEGPWR_REGISTER_ADDR, SET_BYTE)
    
def read_voltage():
    # Beispiel: Lesen der Spannung, Anpassung erforderlich
    
    raw_voltage = bus.read_i2c_block_data(I2C_ADDR, REG_VOLTAGE, 2)
    #print(((raw_voltage[0] << 8) | raw_voltage[1]))
    voltage = FSV*((raw_voltage[0] << 8) | raw_voltage[1])/DENOMINATOR#(raw_voltage/DENOMINATOR)*FSV     #Versorgungsspannung berechnen
    return (round(voltage,2))

def read_current():
    # Beispiel: Lesen des Stroms, Anpassung erforderlich
      
    raw_current = bus.read_i2c_block_data(I2C_ADDR, REG_CURRENT, 2)
    #print(((raw_current[0] << 8) | raw_current[1]))
    current = FSC*((raw_current[0] << 8) | raw_current[1])/DENOMINATOR #
    return (round(current,3))

def read_power():
    # Beispiel: Lesen der Leistung, Anpassung erforderlich
      
    raw_power = bus.read_i2c_block_data(I2C_ADDR, REG_POWER, 4)
    calc_power = raw_power[0]
    calc_power <<=8
    calc_power |= raw_power[1]
    calc_power <<=8
    calc_power |= raw_power[2]
    calc_power <<=4
    raw_power[3] >>=4
    calc_power |= raw_power[3]
    power = POWER_FSR*calc_power / 268435455
    return (round(power,2))
    
def read_energy():
    
    raw_energy = bus.read_i2c_block_data(I2C_ADDR, REG_POWER_ACC, 6)
    acc_count = bus.read_i2c_block_data(I2C_ADDR, REG_ACC_COUNT, 3)
    print(raw_energy)
    print(acc_count)
    int_energy = int.from_bytes(raw_energy, byteorder = 'big')
    int_count = int.from_bytes(acc_count, byteorder = 'big')
    print(int_energy)
    print(int_count)
    energy= (((int_energy/268435455)*POWER_FSR)*(1/1024))*100
    return(round(energy,8))
