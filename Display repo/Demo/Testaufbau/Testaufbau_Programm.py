import PiRelay6
import time

r1 = PiRelay6.Relay("RELAY1")
r2 = PiRelay6.Relay("RELAY2")
r3 = PiRelay6.Relay("RELAY3")
r4 = PiRelay6.Relay("RELAY4")
r5 = PiRelay6.Relay("RELAY5")
r6 = PiRelay6.Relay("RELAY6")


for i in range(1):
		r3.on()
		time.sleep(0.5)
		r3.off()
		
	
		




