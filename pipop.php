<?php

// upload interval, in seconds
$fileMaxAge = 60;

// the destination where the images will be moved
$destinationFolder = "images/";

// if we are not uploading a new image (POST), then try to serve an existing one
if ('POST' !== $_SERVER['REQUEST_METHOD'] && true === isset($_GET['camera'])) {
    $fileHash = sha1($_GET['camera']);
    $fileDestination = $destinationFolder . $fileHash . '.jpg';

    // return 404 of the file is not there
    if (true !== file_exists($fileDestination)) {
        header('X-PHP-Response-Code: 404', true, 404);
        die('Image file not found');
    }

    // get information about the image to construct the necessary http response headers
    $size = filesize($fileDestination);
    $mtime = filemtime($fileDestination);

    // the image expires $fileMaxAge seconds after it was created
    $lastModified = gmdate('D, d M Y H:i:s \G\M\T', $mtime);
    $expires = gmdate('D, d M Y H:i:s \G\M\T', $mtime + $fileMaxAge);

    header('Content-Type: '   . 'image/jpeg');
    header('Content-Length: ' . $size);
    header('Cache-Control: '  . 'public, max-age=' . $fileMaxAge);
    header('Last-Modified: '  . $lastModified);
    header('Expires: '        . $expires);

    header("HTTP/1.1 200 OK");
    readfile($fileDestination);

    // we served the image, so we are done
    die();
}

// shared secret between client and server
$sharedSecret = "556f6ca0435179373326a788a42d559b729e1a50d3aa11a8d7466339a2ccef3b";

// file where successful requests are logged
$logFile = "log.txt";

function isSigned($secret, $filename, $hash) {
    // read the image from the request and base64 encode it
    $content = base64_encode(file_get_contents($filename));
    // calculate the hash of the base64 encoded string
    $calculatedHash = hash_hmac('sha256', $content, $secret);

    // compare if the client sent us the expected hash
    return $hash === $calculatedHash;
}

$hash   = isset($_SERVER['HTTP_X_HASH']) ? $_SERVER['HTTP_X_HASH'] : null;
$camera = isset($_SERVER['HTTP_X_CAMERA']) ? $_SERVER['HTTP_X_CAMERA'] : null;
$file   = isset($_FILES['image']) ? $_FILES['image'] : null;

// bad request from the client
if (null === $file || $file['error'] !== UPLOAD_ERR_OK) {
    header('X-PHP-Response-Code: 500', true, 500);
    die('No file found');
}

// no hash or camera provided by the client
if (null === $hash || null === $camera) {
    header('X-PHP-Response-Code: 401', true, 401);
    die('Move along, nothing to see here');
}

// unauthenticated request from the client
if (false === isSigned($sharedSecret, $file['tmp_name'], $hash)) {
    header('X-PHP-Response-Code: 401', true, 401);
    die('Move along, nothing to see here');
}

// calculate new file name
$fileHash = sha1($camera);
$fileDestination = $destinationFolder . $fileHash . '.jpg';

// log that a succesful request came in
file_put_contents($logFile, date('c') . "\t" . filesize($file['tmp_name']) . " bytes written to {$fileDestination}\n", FILE_APPEND);

// move the file
move_uploaded_file($file['tmp_name'], $fileDestination);

die('OK');
