import smbus2
import tkinter as tk
import threading 
import time
import os
from datetime import datetime
import RPi.GPIO as GPIO
import measurelib
from DRV8825 import DRV8825
from multiprocessing import Process
from enum import Enum


########################################### INITS ############################################
    
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor1.SetMicroStep('hardward' ,'1/4step')
Motor2.SetMicroStep('hardward' ,'1/4step')
Motor1.Stop()
Motor2.Stop()

endschalter=8
GPIO.setup(endschalter,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
channelX=10
GPIO.setup(channelX,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

sole1=14
sole2=23
sole3=5
sole4=6

GPIO.setup(sole1,GPIO.OUT)
GPIO.setup(sole2,GPIO.OUT)
GPIO.setup(sole3,GPIO.OUT)
GPIO.setup(sole4,GPIO.OUT)

masterposition = 0

######################################### FUNKTIONEN #########################################
class Magpositions(Enum):
	magA = 0
	magB = 1066
	magC = 2133
	
class Platepositions(Enum):
	plate1 = 0
	plate2 = 800
	plate3 = 1600
	plate4 = 2400

def messungen_thread():
	while(1):
		measurelib.send_refresh_v_command()
		time.sleep(0.005)

	
		voltage = measurelib.read_voltage()
        
		current = measurelib.read_current()
        
		power = measurelib.read_power()
        
		os.system('clear')
		print(f"Spannung: {voltage} V, Strom: {current} A, Leistung: {power} W")
		time.sleep(0.5)
	
def zero_bed():
	while(GPIO.input(endschalter)==0):
		Motor2.TurnStep(Dir='backward', steps=1, stepdelay=0.00005)
	Motor2.Stop()
	return()
	
def show_bed():
	Motor2.TurnStep(Dir='forward', steps=9000, stepdelay=0.00005)
	Motor2.Stop()
	return()
        
def zero_mag():
	global masterposition
	while(GPIO.input(channelX)==0):
		Motor1.TurnStep(Dir='forward', steps=1, stepdelay=0.00005)
	Motor1.TurnStep(Dir='forward', steps=250, stepdelay=0.00005)
	time.sleep(0.2)
	Motor1.Stop()
	masterposition=0
	return()
	
def place_cube(mag, pos):
	global masterposition
	
	actualpos = masterposition + mag
	if actualpos >= 3200:
		actualpos -= 3200

	
	schritte= pos - actualpos
	if schritte < 0 :
		schritte = 3200 - abs(schritte)
	

	Motor1.TurnStep(Dir='forward', steps=schritte, stepdelay=0.00005)
	
	
	if pos == 0:
		GPIO.output(sole1,1)
		time.sleep(0.1)
		GPIO.output(sole1,0)
	elif pos == 800:
		GPIO.output(sole2,1)
		time.sleep(0.1)
		GPIO.output(sole2,0)
	elif pos == 1600:
		GPIO.output(sole3,1)
		time.sleep(0.1)
		GPIO.output(sole3,0)
	elif pos == 2400:
		GPIO.output(sole4,1)
		time.sleep(0.1)
		GPIO.output(sole4,0)
	
	time.sleep(0.1)
	masterposition += schritte
	if masterposition >= 3200:
		masterposition -= 3200
	return()
	
        ######################################### CODE ###########################################

zero_bed()
	
zero_mag()

measurelib.send_ctrlreg_command()
measurelib.send_chdis_command()
measurelib.send_negpwr_command()
measurelib.send_refresh_command()
startTime = datetime.now()

if __name__=='__main__':	
	
	messen = Process(target=messungen_thread)
	messen.start()

	

	
	
	
	place_cube(Magpositions.magA.value, Platepositions.plate2.value)
	place_cube(Magpositions.magA.value, Platepositions.plate1.value)
	place_cube(Magpositions.magC.value, Platepositions.plate1.value)
	place_cube(Magpositions.magC.value, Platepositions.plate4.value)
	place_cube(Magpositions.magB.value, Platepositions.plate3.value)
	place_cube(Magpositions.magB.value, Platepositions.plate4.value)
	place_cube(Magpositions.magA.value, Platepositions.plate2.value)
	place_cube(Magpositions.magA.value, Platepositions.plate3.value)
	Motor1.Stop()
	


	
	show_bed()
	
	
	

	

     ######################################### SCHLUSS ###########################################
	messen.terminate()
	energy = measurelib.read_energy()

	
	print(f"Energie: {energy} Ws : {energy/3600} Wh")
	

	print(f"Aufbauzeit: {datetime.now() - startTime}")
	time.sleep(5)
	
	GPIO.cleanup()
	
