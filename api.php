<?php

// shared secret between client and server
$sharedSecret = "556f6ca0435179373326a788a42d559b729e1a50d3aa11a8d7466339a2ccef3b";

// the destination where the image will be moved
$fileDestination = "/tmp/image.jpg";

// file where successful requests are logged
$logFile = "/tmp/log.txt";


function isSigned($secret, $filename, $hash) {
    // read the image from the request and base64 encode it
    $content = base64_encode(file_get_contents($filename));
    // calculate the hash of the base64 encoded string
    $calculatedHash = hash_hmac('sha256', $content, $secret);

    // compare if the client sent us the expected hash
    return $hash === $calculatedHash;
}


$hash = isset($_SERVER['HTTP_X_HASH']) ? $_SERVER['HTTP_X_HASH'] : null;
$file = isset($_FILES['image']) ? $_FILES['image'] : null;


if (null === $file || $file['error'] !== UPLOAD_ERR_OK) {
    die('no file found');
}

if (null === $hash) {
    die('move along, nothing to see here');
}

if (false === isSigned($sharedSecret, $file['tmp_name'], $hash)) {
    die('move along, nothing to see here');
}

// log that a succesful request came in
file_put_contents($logFile, date('c') . " || " . filesize($file['tmp_name']) . " bytes\n", FILE_APPEND);

// move the file
move_uploaded_file($file['tmp_name'], $fileDestination);

die('ok');
