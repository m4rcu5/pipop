#!/usr/bin/env python
import time
import atexit
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# Let's use BCM numbers
GPIO.setmode(GPIO.BCM)

# Channels needed
channels = [19, 20]

# Initialize channels
GPIO.setup(channels, GPIO.OUT, initial=GPIO.LOW)

# Clean up our mess
def cleanup():
	GPIO.cleanup(channels)

atexit.register(cleanup)

#
# Main loop
#
while True:
	print('Focusing...')

	GPIO.output(19, GPIO.HIGH)
	time.sleep(2)

	print('Taking image!')
	GPIO.output(20, GPIO.HIGH)
	time.sleep(0.5)

	GPIO.output([19, 20], GPIO.LOW)

	# read before next shot
	raw_input("Press Enter to do another...")
