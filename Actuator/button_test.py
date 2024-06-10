import RPi.GPIO as gpio
import time

buttonPin = 23

gpio.setmode(gpio.BCM)
gpio.setup(buttonPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)

while True:
#	print("Loop")
	
	if gpio.input(buttonPin) == gpio.LOW:
		print("no")
	else:
		print("Button was pressed")
#		break
