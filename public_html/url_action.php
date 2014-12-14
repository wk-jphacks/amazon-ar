<?php
// url
$url = $_GET['url'];
// img processing
system("(cd ../scripts; python item_info.py $url;");
// img_nm converted to sha
$img_nm = sha1($url) . '.png';
// get item size
$f = fopen('img/'.$img_nm.'_size.csv', 'r');
$size_txt = fread($f, filesize('img/'.$img_nm.'_size.csv'));
$pieces = explode(",", $size_txt);
$height = floatval($pieces[0]);
$weight = floatval($pieces[1]);
$depth = floatval($pieces[2]);
fclose($f);
// redirect
header("Location: index.html?img=$img_nm&width=$width&height=$height&depth=$depth");
