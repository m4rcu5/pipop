#!/usr/bin/env python
import os
import sys
import time
import logging
import atexit

base_dir = os.path.abspath(os.path.dirname(__file__))
pid_file = os.path.join(base_dir, 'pipop.pid')

# Logging
logging.basicConfig(
    filename=os.path.join(base_dir, 'pipop.log'),
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

cameraName = os.uname()[1]

# Say hello to the log
logging.info('Starting up!')

#
# PIDfile handing, there should only be one instance
#
if os.path.exists(pid_file):
    pid = int((open(pid_file).read()))

    logging.error('PIDfile found for pid: ' + str(pid))

    try:
        os.kill(pid, 0)
    except OSError:
        logging.error('Process seems to have died.')
    else:
        logging.error('Attempting to kill and continue...')

        try:
            os.kill(pid, signal.SIGKILL)
        except OSError as e:
            logging.critical("Could not kill proccess! : " + e.message)

# If we are here the PIDfile is invalid, writing PID for new script process
open(pid_file, 'w').write(str(os.getpid()))

def removePIDfile():
    logging.debug('Removing PIDfile')

    os.remove(pid_file)

atexit.register(removePIDfile)

#
# Image capturing
#
import subprocess
from wand.image import Image

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

#
# Image processing
#
logging.info('Resizing image...')

# Resize our image to a usage dimension
img.resize(imgWidth, imgHeight)


#
# Images Shipping
#
import hmac
import base64
import hashlib
import requests

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
    headers={
        'x-hash': hash,
        'x-camera': cameraName
    }
)

logging.info('Response form server: ' + response.text)

## End of process
logging.info('Shutting down!')
