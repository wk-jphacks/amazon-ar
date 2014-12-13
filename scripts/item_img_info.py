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
    img = img[:, :, ::-1].copy()

    # get contour
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgray = cv2.GaussianBlur(imgray, (9, 9), 0)
    ret, thresh = cv2.threshold(imgray, 0, 255,
            cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_with_contours = img.copy()
    cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 1)
    # debugging
    cv2.imshow('with contours', img_with_contours)
    cv2.waitKey()

    # debugging
    cv2.imwrite('ignore/original.png', img)
    cv2.imshow('original', img)
    cv2.waitKey()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    else:
        url = 'http://www.amazon.co.jp/%E4%B8%8D%E4%BA%8C%E8%B2%BF%E6%98%93-%E3%83%95%E3%83%AA%E3%83%BC%E3%83%9C%E3%83%83%E3%82%AF%E3%82%B9-FBC960-%E3%82%AB%E3%83%A9%E3%83%BC%E3%83%9C%E3%83%83%E3%82%AF%E3%82%B9-57093/dp/B00163JL6E/ref=sr_1_3?s=home&ie=UTF8&qid=1418455551&sr=1-3&keywords=%E6%A3%9A'

    get_item_img_info(url=url)

