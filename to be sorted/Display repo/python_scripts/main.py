#!/usr/bin/python

import threading
import time

# from pca9685 import PCA9685  # Import der PCA9685 Klasse
import PiRelay6
import RPi.GPIO as GPIO
from DRV8825 import DRV8825


def relais():
    r1 = PiRelay6.Relay("RELAY1")
    r2 = PiRelay6.Relay("RELAY2")
    r3 = PiRelay6.Relay("RELAY3")
    r4 = PiRelay6.Relay("RELAY4")
    r5 = PiRelay6.Relay("RELAY5")
    r6 = PiRelay6.Relay("RELAY6")
    for i in range(1):
        r1.on()
        time.sleep(0.1)
        r2.on()
        time.sleep(0.1)
        r3.on()
        time.sleep(0.1)
        r4.on()
        time.sleep(0.1)
        r5.on()
        time.sleep(0.1)
        r6.on()
        time.sleep(0.7)
        r1.off()
        time.sleep(0.1)
        r2.off()
        time.sleep(0.1)
        r3.off()
        time.sleep(0.1)
        r4.off()
        time.sleep(0.1)
        r5.off()
        time.sleep(0.1)
        r6.off()
        time.sleep(0.7)

    print("relais done")


"""
def servo():
    
    for i in range(10):
        pwm.setServoPulse(0,500)   
        time.sleep(1)
        pwm.setServoPulse(0,2500)   
        time.sleep(1)
        
    pwm.setServoPulse(0,0)
    print("servo done")
"""


def motor1():
    print("init motor")
    Motor1 = DRV8825(dir_pin=36, step_pin=38, enable_pin=32, mode_pins=(18, 18, 18))
    print("set steps")
    Motor1.SetMicroStep("hardward", "1/8step")
    print("start motor")
    Motor1.TurnStep(Dir="forward", steps=10000, stepdelay=0.0001)
    Motor1.Stop()


def motor2():
    print("init motor")
    Motor2 = DRV8825(dir_pin=18, step_pin=13, enable_pin=7, mode_pins=(16, 16, 16))
    print("set steps")
    Motor2.SetMicroStep("hardward", "1/8step")
    print("start motor")
    Motor2.TurnStep(Dir="forward", steps=10000, stepdelay=0.0001)
    Motor2.Stop()


if __name__ == "__main__":

    # Erstellen von Threads für jede Funktion
    thread1 = threading.Thread(target=relais)
    thread2 = threading.Thread(target=motor1)
    thread3 = threading.Thread(target=motor2)

    # Starten der Threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Warten auf das Ende der Threads
    thread1.join()
    thread2.join()
    thread3.join()

    print("Threading Beispiel beendet.")

"""
    try:
        print("init motor")
        #Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        Motor1 = DRV8825(dir_pin=33, step_pin=35, enable_pin=32, mode_pins=(36, 11, 38))
        #Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        Motor2 = DRV8825(dir_pin=18, step_pin=12, enable_pin=7, mode_pins=(40, 15, 13))
        print("set steps")
        Motor2.SetMicroStep('hardward' ,'1/8step')
        print("start motor")
        Motor2.TurnStep(Dir='forward', steps=10000, stepdelay=0.0001)
        Motor2.Stop()
    
    
    except:
        # GPIO.cleanup()
        print("\nMotor stop")
        Motor1.Stop()
        Motor2.Stop()
        exit()
"""

"""    while True:
        pwm.setServoPulse(0,1540)
        print("wait")
        time.sleep(5)
        
        for i in range(1300,1700,10):  
            pwm.setServoPulse(0,i)   
            time.sleep(0.005)  
            print(f"i: {i}")   
    
        for i in range(1700,1300,-10):
            pwm.setServoPulse(0,i) 
            time.sleep(0.005)
            print(f"i: {i}")  
        
        pwm.setServoPulse(0,1540)
        print("wait")
        time.sleep(1)
    
        r1 = PiRelay6.Relay("RELAY1")
        for i in range(10):
            r1.on()
            time.sleep(0.1)
            r1.off()
            time.sleep(0.1)"""
