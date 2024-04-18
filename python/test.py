import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825


try:
	Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
	Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
	Motor2.SetMicroStep('hardward' ,'1/8step')
	"""
	# 1.8 degree: nema23, nema14
	# softward Control :
	# 'fullstep': A cycle = 200 steps
	# 'halfstep': A cycle = 200 * 2 steps
	# '1/4step': A cycle = 200 * 4 steps
	# '1/8step': A cycle = 200 * 8 steps
	# '1/16step': A cycle = 200 * 16 steps
	# '1/32step': A cycle = 200 * 32 steps
	"""
	
	
	text = 2
	schritte = 16000
	schrittdelay =1000
	
	while(text != ""):
		print("Press Enter:")
		text = input()
		time.sleep(0.1)
	while True:	
			for i in range(schritte):
				Motor2.TurnStep(Dir='forward', steps=10000, stepdelay=(0.005))
				schrittdelay = schrittdelay + (300000/schritte)
				print(schrittdelay)
			time.sleep(0.1)
			Motor2.Stop()
			print(schrittdelay)
			schrittdelay = 1000
			time.sleep(1)
	text = 2

	0.00000333
	
	"""
	# 28BJY-48:
	# softward Control :
	# 'fullstep': A cycle = 2048 steps
	# 'halfstep': A cycle = 2048 * 2 steps
	# '1/4step': A cycle = 2048 * 4 steps
	# '1/8step': A cycle = 2048 * 8 steps
	# '1/16step': A cycle = 2048 * 16 steps
	# '1/32step': A cycle = 2048 * 32 steps
	"""
	
	
	

except:
    # GPIO.cleanup()
    print("\nMotor stop")
    Motor1.Stop()
    Motor2.Stop()
    exit()
