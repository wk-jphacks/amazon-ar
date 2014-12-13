<?php
$url = $_GET['url'];
/*$width = $_GET['width'];
$height = $_GET['height'];
$depth = $_GET['depth'];*/

//system("python ../scripts/get_image.py $url");
$img = sha1($url) . '.png';

header("Location: index.html?img=$img&width=$width&height=$height&depth=$depth");
