# PiPOP - Bevrijdingspop Timelapse Camera

The Bevrijdingspop Timelapse Camera project aka PiPOP, is a combination of scripts to take images and upload them to a web page.

## Components
- `pipop-usb.py`: The Python script which takes the image, processes it and uploads it to an API endpoint.
- `pipop.php`: The PHP script which accepts the image on POST requests, saves it to disk and on GET requests serves it to the visitor.

## Requirements

`gphoto`, `python` and the following modules:

- `Wand` for image processing
- `Requests` for uploading the image

## Installation

### Scripts
#### `pipop.php`
1. Copy the `pipop.php` file to an accessible and writable directory on your web-server.
2. Change the `$fileMaxAge` to the intended interval.
3. change the `$sharedSecret` to a secret of your own, save it for the `pipop-usb.py` setup.
4. Create the `./images/` folder on the webserver and make sure the webserver can write to it.

#### `pipop-usb.py`
1. Make sure you installed the requirements as listed above.
2. Copy the `pipop-usb.py` to a writable folder on your machine (or Raspberry as the name implies).
3. Set `imgWidth` and `imgHeight` to the intended image size.
4. Set the `imageServer` to the url of the API endpoint, and `sharedSecret` to the noted down secret.
5. Optionally set the `cameraName` to a static value.

For the best result, set up a cronjob to run at the intended interval.

## Usage

To display the captured image on your site, you should call the `pipop.php` script with the query variable `camera`. This will display the correct camera image and make sure the cache headers are set correctly.
Example: `pipop.php?camera=pipop01`

## Hardware
Connect your camera via USB to the system. For the best results I would recommend setting it to manual focus.

The rest should be handled by the script.

## Authors

- Marcus van Dam (marcus _at_ marcusvandam.nl)
- Nico Di Rocco
