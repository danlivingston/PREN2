import os
import subprocess
import RPi.GPIO as GPIO
from DRV8825 import DRV8825

# Initialize Motor2
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor2.SetMicroStep('hardware', '1/4step')
Motor2.Stop()

# Setup GPIO for the end switch
endschalter = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(endschalter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

sole1=14
sole2=23
sole3=5
sole4=6

GPIO.setup(sole1,GPIO.OUT)
GPIO.setup(sole2,GPIO.OUT)
GPIO.setup(sole3,GPIO.OUT)
GPIO.setup(sole4,GPIO.OUT)

# Function to zero the bed using Motor2
def show_bed():
    Motor2.TurnStep(Dir='forward', steps=9000, stepdelay=0.00005)
    Motor2.Stop()

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    first_script_path = os.path.join(base_dir, 'visual', 'resetvisual.py')
    first_script_process = subprocess.Popen(['python', first_script_path])

    try:
        show_bed()  # Zero the bed on start using Motor2

    except KeyboardInterrupt:
        print("Process manually interrupted.")
        Motor2.Stop()
    finally:
        first_script_process.terminate()
        try:
            first_script_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            first_script_process.kill()
        GPIO.cleanup()
        print("Cleanup complete and program terminated.")
