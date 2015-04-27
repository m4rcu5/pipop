#!/usr/bin/env python
import time
import atexit
import logging
import RPi.GPIO as GPIO

# Logging
logging.basicConfig(
	filename='pipop.log',
	level=logging.DEBUG,
	format='%(asctime)s %(message)s'
)

logging.info('Starting up!')

# GPIO might already be initialized
GPIO.setwarnings(False)

# Let's use BCM numbers
GPIO.setmode(GPIO.BCM)

# Channels needed
cameraFocus   = 19
cameraTrigger = 20

# Initialize channels
GPIO.setup([cameraTrigger, cameraFocus], GPIO.OUT, initial=GPIO.LOW)

# Clean up our mess
def cleanup():
	GPIO.cleanup([cameraTrigger, cameraFocus])

atexit.register(cleanup)

#
# Trigger camera (FAIL SAVE)
#

logging.info('Focusing...')

GPIO.output(cameraFocus, GPIO.HIGH)
time.sleep(2)

logging.info('Taking image!')
GPIO.output(cameraTrigger, GPIO.HIGH)
time.sleep(0.5)

GPIO.output([cameraFocus, cameraTrigger], GPIO.LOW)

#
#
#

