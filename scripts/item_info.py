#!/usr/bin/env python
# -*- coding: utf-8 -*-
# item_info.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import os
import sys
import re
import time
from StringIO import StringIO

import requests
from bs4 import BeautifulSoup

import numpy as np
from PIL import Image
import cv2
from termcolor import cprint


def get_size_info(soup, pattern):
    if pattern == 0:
        elm = soup.find('div', {'id': 'feature-bullets'})
        if (elm is None) or (len(elm) == 0):
            return None
        spans = elm.find_all('span', {'class': 'a-list-item'})
        if len(spans) == 0:
            return None
        size_texts = [span.get_text() for span in spans if u'cm' in span.get_text()]
        if len(size_texts) == 0:
            return None
        size_text = size_texts[0]
        if u'×' in size_text:
            size_text_splitted = size_text.split(u'×')
        elif u'x' in size_text:
            size_text_splitted = size_text.split(u'x')
        else:
            return None
        size_info = []
        for spl in size_text_splitted:
            size_info.append(float(re.findall(r'\d+\.?\d*', spl)[0]))
        return size_info
    elif pattern == 1:
        trs = soup.find_all('tr', {'class': 'size-weight'})
        if len(trs) == 0:
            return None
        size_text = [tr.get_text() for tr in trs if u'cm' in tr.get_text()][0]
        if u'×' in size_text:
            size_text_splitted = size_text.split(u'×')
        elif u'x' in size_text:
            size_text_splitted = size_text.split(u'x')
        else:
            return None
        size_info = []
        for spl in size_text_splitted:
            size_info.append(float(re.findall(r'\d+\.?\d*', spl)[0]))
        return size_info


def get_item_info(url):
    # get item image from amazon
    t_start = time.time()
    while time.time() - t_start < 20:
        r = requests.get(url)
        if r.status_code == 200:
            break
    soup = BeautifulSoup(r.text.encode(r.encoding))

    size_info = get_size_info(soup, pattern=0)
    if size_info is not None:
        return size_info

    size_info = get_size_info(soup, pattern=1)
    if size_info is not None:
        return size_info


if __name__ == '__main__':
    urls = [
            'http://www.amazon.co.jp/Home-%E3%83%95%E3%82%A1%E3%83%96%E3%82%B6%E3%83%9B%E3%83%BC%E3%83%A0%E3%80%91-%E3%82%B3%E3%83%B3%E3%83%95%E3%82%A9%E3%83%BC%E3%82%BF%E3%83%BC%E3%82%AB%E3%83%90%E3%83%BCS-150x210cm-FH121156-240/dp/B00O41CTL4/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1418480912&sr=1-1',
            'http://www.amazon.co.jp/gp/product/B00KS1NWHO/ref=s9_hps_gw_g147_i5?pf_rd_m=AN1VRQENFRJN5&pf_rd_s=center-6&pf_rd_r=0DPJNEJ1CR3TZGW53S6Z&pf_rd_t=101&pf_rd_p=188675289&pf_rd_i=489986',
            ]

    for url in urls:
        cprint(get_item_info(url=url), color='yellow')
        print url
