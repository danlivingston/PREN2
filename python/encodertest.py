import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

import threading

GPIO.setmode(GPIO.BCM)
channelA=6
channelB=5
channelX=10

"""
sole1=14
sole2=23
sole3=5
sole4=6

GPIO.setup(sole1,GPIO.OUT, initial=0)
GPIO.setup(sole2,GPIO.OUT, initial=0)
GPIO.setup(sole3,GPIO.OUT, initial=0)
GPIO.setup(sole4,GPIO.OUT, initial=0)
"""
GPIO.setup(channelA,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(channelB,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(channelX,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor1.SetMicroStep('hardward' ,'1/4step')





def angle_print():
	wert = 1
	old_state=0
	new_state=0
	valueA = False
	valueB = False
	
	while(1):
		
		valueA = GPIO.input(channelA)
		valueB = GPIO.input(channelB)
	
	
		if(valueA & (not(valueB))):
			new_state= 1
		if(valueA & valueB):
			new_state= 2
		if((not (valueA)) & valueB):
			new_state= 3
		if((not (valueA)) & (not(valueB))):
			new_state= 4
	
	
		if(new_state != old_state):
			wert += 1
			old_state = new_state
		
		print(f"{round(wert*0.9375,1)}      ", end='\r')
		
x = threading.Thread(target=angle_print)
#x.start()

def go_home():
	while(GPIO.input(channelX)==0):
		Motor1.TurnStep(Dir='forward', steps=1, stepdelay=0.00005)
	print("home")
	time.sleep(0.5)
	Motor1.Stop()
	time.sleep(1.5)
	return()
	
	
stepcount=0
itercount=0
go_home()
while(1):
	
	while(itercount<15):
		Motor1.TurnStep(Dir='forward', steps=800, stepdelay=0.00005)
		itercount +=1
		time.sleep(0.5)
	

	while(GPIO.input(channelX)==0):
		Motor1.TurnStep(Dir='forward', steps=1, stepdelay=0.00005)
		stepcount +=1
	print(stepcount)
	stepcount=0
	itercount=0
	time.sleep(0.2)
	Motor1.Stop()
	time.sleep(0.5)
	

"""
	if GPIO.input(channelX)==1:
		time.sleep(0.1)
		Motor1.Stop()
		wert=1
		time.sleep(1)
		Motor1.TurnStep(Dir='forward', steps=10, stepdelay=0.0005)
		"""
		
		
		#Motor1.Stop()
		#time.sleep(1)
		#Motor1.TurnStep(Dir='forward', steps=100, stepdelay=0.0007)
		#Motor2.TurnStep(Dir='forward', steps=20, stepdelay=0.0005)
		
	
