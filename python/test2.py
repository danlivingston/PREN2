import RPi.GPIO as GPIO
import PiRelay6
import time
from DRV8825 import DRV8825
	
import importlib.util
import pkgutil

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
	

	

	Motor2.TurnStep(Dir='forward', steps=200, stepdelay=0.0005)
	time.sleep(0.5)
	Motor2.Stop()
	
	r1.on()
	time.sleep(0.5)
	r1.off()
	time.sleep(0.5)
	


	
	



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
	def list_imported_module_paths():
		imported_modules = list(set(sys.modules) & set(globals()))
		print("Importierte Module und ihre Pfade:")
		for module_name in imported_modules:
			if module_name not in ['_builtins_', 'sys', 'pkgutil', 'importlib.util']:
				module = sys.modules[module_name]
				try:
					print(f"{module_name}: {module._file_}")
				except AttributeError:
					print(f"{module_name}: Built-in Modul oder Pfad nicht verfügbar")

	if _name_ == "_main_":
		import PiRelay6
		list_imported_module_paths()
	
	

except:
    GPIO.cleanup()
    print("\nMotor stop")
    Motor1.Stop()
    Motor2.Stop()
    exit()


