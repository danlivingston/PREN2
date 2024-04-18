import RPi.GPIO as GPIO
import time




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


sole1=14

sole2=23
sole3=5
sole4=6
end=8
GPIO.setup(end,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sole1,GPIO.OUT)

GPIO.setup(sole2,GPIO.OUT)
GPIO.setup(sole3,GPIO.OUT)
GPIO.setup(sole4,GPIO.OUT)

GPIO.output(sole1,1)
time.sleep(1)
GPIO.output(sole1,0)
time.sleep(1)

GPIO.output(sole2,1)
time.sleep(1)
GPIO.output(sole2,0)
time.sleep(1)

GPIO.output(sole3,1)
time.sleep(1)
GPIO.output(sole3,0)
time.sleep(1)

GPIO.output(sole4,1)
time.sleep(1)
GPIO.output(sole4,0)
time.sleep(1)
while(1):
	print(GPIO.input(end))
	time.sleep(1)
