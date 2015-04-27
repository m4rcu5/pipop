#!/usr/bin/env python
import os
import sys
import time
import hmac
import base64
import hashlib
import requests
import subprocess
import logging
from wand.image import Image

# Logging
logging.basicConfig(
	filename='pipop.log',
	level=logging.INFO,
	format='%(asctime)s %(message)s'
)

#
# Variables
#

# Image dimensions
imgWidth = 800
imgHeight = 600

# Server address and secret
imageServer = 'http://imgur.mydomain.tld/api.php'
sharedSecret = '556f6ca0435179373326a788a42d559b729e1a50d3aa11a8d7466339a2ccef3b'

#
# Main Camera Processes
#

## Start of process
logging.info('Starting up!')

logging.info('Taking image...')

# Request gphoto2 to take an image
gphoto2Process = subprocess.Popen(
	["gphoto2", "--set-config", "capturetarget=1", "--capture-image-and-download", "--keep", "--stdout"],
	stdout=subprocess.PIPE,
	stderr=subprocess.PIPE
)

stdOut, stdErr = gphoto2Process.communicate()

# Verify the gphoto2 return code
if gphoto2Process.returncode != 0:
	logging.critical("gphoto2 did not exit successfull: " + stdErr.strip())
	sys.exit(1)
else:
	logging.info(stdErr.strip())

logging.info('Loading image...')

# Not all errors of gphoto2 can be catched!
try:
	img = Image(blob=stdOut)
except Exception as e:
	logging.critical("Wand image processing error: " + e.message)
	sys.exit(1)


logging.info('Resizing image...')

# Resize our image to a usage dimension
img.resize(imgWidth, imgHeight)


#
# Images Shipping
#

logging.info('Shipping image...')

# Convert image back to blob
imgBlob = img.make_blob()

# Encode image for hashing
encoded_string = base64.b64encode(imgBlob)

# Create HMAC secret
hash = hmac.new(sharedSecret, encoded_string, hashlib.sha256).hexdigest()

# POST to server
response = requests.post(
	imageServer,
	files={'image': imgBlob},
	headers={'x-hash': hash}
)

logging.info('Response form server: ' + response.text)

## End of process
logging.info('Shutting down!')
