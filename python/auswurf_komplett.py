import RPi.GPIO as GPIO
import PiRelay6
import time
from DRV8825 import DRV8825


r1 = PiRelay6.Relay("RELAY1")
r2 = PiRelay6.Relay("RELAY2")
r3 = PiRelay6.Relay("RELAY3")
r4 = PiRelay6.Relay("RELAY4")


try:
	
	Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
	Motor2.SetMicroStep('hardward' ,'1/4step')
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
	
	
	verzogerung = 0.0005	#0.0005
	delayhinten = 0.1
	delayvorne = 0.2
	delaywait = 0.01
	
	#Schacht1

	
	Motor2.TurnStep(Dir='forward', steps=800, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r1.on()
	time.sleep(delayhinten)
	r1.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r4.on()
	time.sleep(delayhinten)
	r4.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r3.on()
	time.sleep(delayhinten)
	r3.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r2.on()
	time.sleep(delayhinten)
	r2.off()
	time.sleep(delayvorne)
	
	
	#Schacht 2
	
	Motor2.TurnStep(Dir='forward', steps=467, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r1.on()
	time.sleep(delayhinten)
	r1.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r4.on()
	time.sleep(delayhinten)
	r4.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r3.on()
	time.sleep(delayhinten)
	r3.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r2.on()
	time.sleep(delayhinten)
	r2.off()
	time.sleep(delayvorne)
	
	#Schacht 3
	
	Motor2.TurnStep(Dir='forward', steps=467, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r1.on()
	time.sleep(delayhinten)
	r1.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r4.on()
	time.sleep(delayhinten)
	r4.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r3.on()
	time.sleep(delayhinten)
	r3.off()
	time.sleep(delayvorne)
	
	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
	time.sleep(delaywait)
	
	r2.on()
	time.sleep(delayhinten)
	r2.off()
	time.sleep(delayvorne)
	

	
	Motor2.Stop()
	



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
    GPIO.cleanup()
    print("\nMotor stop")
    Motor1.Stop()
    Motor2.Stop()
    exit()
