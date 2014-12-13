#!/usr/bin/env python
# -*- coding:utf-8 -*-
# product_info.py

# standard libraries
import os
import sys
import time
from StringIO import StringIO

import requests
from bs4 import BeautifulSoup

import numpy as np
from PIL import Image
import cv2


def get_item_img_info(url):
    # get item image from amazon
    t_start = time.time()
    while time.time() - t_start < 10:
        r = requests.get(url)
        if r.status_code == 200:
            break
    soup = BeautifulSoup(r.text.encode(r.encoding))
    elm = soup.find('img', {'id': 'landingImage'})
    imgs = eval(elm.get('data-a-dynamic-image'))
    # get largest img
    img_url = sorted([(h*w, url) for url, (h, w) in imgs.items()])[-1][1]

    # download & load img as numpy.array
    r = requests.get(img_url)
    img = Image.open(StringIO(r.content))
    img = np.array(img)

    # get contour
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh,
            cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_with_contour = img.copy()
    cv2.drawContours(img_with_contour, contours, -1, (0, 255, 0), 3)
    cv2.imshow('with contour', img_with_contour)

    # debugging
    cv2.imwrite('ignore/original.png', img)
    cv2.imshow('original', img)
    cv2.waitKey()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    else:
        url = 'http://www.amazon.co.jp/A4%E6%9B%B8%E6%A3%9A-A4%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%B0%82%E7%94%A8%E6%9B%B8%E6%A3%9A-5%E6%AE%B5-%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88-59009/dp/B005J1MKJY/ref=sr_1_15?s=home&ie=UTF8&qid=1418437401&sr=1-15'

    get_item_img_info(url=url)

