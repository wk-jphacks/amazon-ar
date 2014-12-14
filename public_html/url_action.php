<?php
// url
$url = $_GET['url'];
// img processing
exec("python /home/ubuntu/amazon-ar/scripts/item_info.py \"$url\"");
// get item size
$img_nm = md5($url);
$f = fopen('img/'.$img_nm.'_size.csv', 'r');
$size_txt = fread($f, filesize('img/'.$img_nm.'_size.csv'));
$pieces = explode(",", $size_txt);
$width = floatval($pieces[0]);
$depth = floatval($pieces[1]);
$height = floatval($pieces[2]);
fclose($f);
# generate qr code
$ar_url = "http://amazon-ar.ddo.jp/ar/?sha=$img_nm&width=$width&height=$height&depth=$depth";
exec("qr \"$ar_url\" > img/".$img_nm."_qr.png");
// redirect
header("Location: $ar_url");
