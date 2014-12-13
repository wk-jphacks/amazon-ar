#!/usr/bin/env python
# -*- coding:utf-8 -*-
# product_info.py

# standard libraries
import os
import sys
from StringIO import StringIO

import requests
from bs4 import BeautifulSoup

import numpy as np
from PIL import Image
import cv2


def get_product_info(url):
    # get item image from amazon
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode(r.encoding))
    elm = soup.find('img', {'id': 'landingImage'})
    imgs = eval(elm.get('data-a-dynamic-image'))
    # get largest img
    img_url = sorted([(h*w, url) for url, (h, w) in imgs.items()])[-1][1]

    # download & load img as numpy.array
    r = requests.get(img_url)
    img = Image.open(StringIO(r.content))
    img = np.array(img)

    # debugging
    cv2.imwrite('ignore/original.png', img)
    cv2.imshow('original', img)
    cv2.waitKey()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    else:
        url = 'http://www.amazon.co.jp/A4%E6%9B%B8%E6%A3%9A-A4%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%B0%82%E7%94%A8%E6%9B%B8%E6%A3%9A-5%E6%AE%B5-%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88-59009/dp/B005J1MKJY/ref=sr_1_15?s=home&ie=UTF8&qid=1418437401&sr=1-15'

    get_product_info(url=url)

