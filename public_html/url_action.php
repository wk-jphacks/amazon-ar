<?php
// url
$url = $_GET['amazonItemUrl'];
$marker_size = $_GET['markerSize'] * 10;
$http_referer = $_SERVER['HTTP_REFERER'];
// img processing
exec('python ' . dirname(__FILE__) . "/../scripts/item_info.py '$url'");
// get item size
$img_nm = md5($url);
$f = fopen('img/'.$img_nm.'_size.csv', 'r');
$size_txt = fread($f, filesize('img/'.$img_nm.'_size.csv'));
$pieces = explode(',', $size_txt);
$width = floatval($pieces[0]);
$depth = floatval($pieces[1]);
$height = floatval($pieces[2]);
fclose($f);
# generate qr code
$ar_url = $http_refererar . "ar/?msize=$marker_size&img=$img_nm&width=$width&height=$height&depth=$depth";
exec("qr \"$ar_url\" > img/" . $img_nm . "_qr.png");
// redirect
header("Location: $ar_url");
