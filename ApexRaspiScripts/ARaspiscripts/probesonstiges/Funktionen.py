import RPi.GPIO as GPIO
import PiRelay6
import time
from DRV8825 import DRV8825

# Initialisierung der Stössel
r1 = PiRelay6.Relay("RELAY1")
r2 = PiRelay6.Relay("RELAY2")
r3 = PiRelay6.Relay("RELAY3")
r4 = PiRelay6.Relay("RELAY4") 

# Initialisierung des Steppermotors
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor2.SetMicroStep('hardward', '1/4step')

verzogerung = 0.0005  # Verzögerung zwischen den Steps

def stossel_ansteuern(stossel):
    if stossel == 1:
        r1.on()
        time.sleep(0.1)
        r1.off()
    elif stossel == 2:
        r2.on()
        time.sleep(0.1)
        r2.off()
    elif stossel == 3:
        r3.on()
        time.sleep(0.1)
        r3.off()
    elif stossel == 4:
        r4.on()
        time.sleep(0.1)
        r4.off()

def motor_steps(steps):
    Motor2.TurnStep(Dir='forward', steps=steps, stepdelay=verzogerung)
    Motor2.Stop()

def motor_stop():
    Motor2.Stop()


# Berechnung der Schritte für eine vollständige Umdrehung
SCHRITTE_PRO_UMDREHUNG = 800

def drehen_um_grad(grad):
    schritte = int((SCHRITTE_PRO_UMDREHUNG / 360) * grad)
    motor_steps(schritte)
    motor_stop()  # Motor abschalten nach der Bewegung


##def notaus():
    #print("NOTAUS aktiviert")
    #motor_stop()
    #for i in range(1, 5):
        #stossel_ansteuern(i, ein=False)  # Annahme, dass es eine Option zum Ausschalten gibt



def kompletter_durchlauf():
    try:
        verzogerung = 0.0005  # Verzögerung zwischen den Steps
        delay_hinten = 0.1
        delay_vorne = 0.2

        # Initialisierung des Motors
        Motor2.SetMicroStep('hardware', '1/4step')

        #Schacht1

        Motor2.TurnStep(Dir='forward', steps=800, stepdelay=verzogerung)
        time.sleep(0.1)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r1.on()
        time.sleep(delay_hinten)
        r1.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r4.on()
        time.sleep(delay_hinten)
        r4.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r3.on()
        time.sleep(delay_hinten)
        r3.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r2.on()
        time.sleep(delay_hinten)
        r2.off()
        time.sleep(delay_vorne)
        
        
        #Schacht 2
        
        Motor2.TurnStep(Dir='forward', steps=467, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r1.on()
        time.sleep(delay_hinten)
        r1.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r4.on()
        time.sleep(delay_hinten)
        r4.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r3.on()
        time.sleep(delay_hinten)
        r3.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r2.on()
        time.sleep(delay_hinten)
        r2.off()
        time.sleep(delay_vorne)
        
        #Schacht 3
        
        Motor2.TurnStep(Dir='forward', steps=467, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r1.on()
        time.sleep(delay_hinten)
        r1.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r4.on()
        time.sleep(delay_hinten)
        r4.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r3.on()
        time.sleep(delay_hinten)
        r3.off()
        time.sleep(delay_vorne)
        
        Motor2.TurnStep(Dir='forward', steps=200, stepdelay=verzogerung)
        time.sleep(0.1)
        
        r2.on()
        time.sleep(delay_hinten)
        r2.off()
        time.sleep(delay_vorne)

        
        Motor2.Stop()



    except Exception as e:
        print(f"Fehler: {e}")
        GPIO.cleanup()
        Motor2.Stop()
