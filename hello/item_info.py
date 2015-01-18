#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

__author__ = 'www.kentaro.wada@gmail.com (Kentaro Wada)'


import sys;
sys.path.insert(0, 'libs')

import os
import re
import time
import hashlib
from StringIO import StringIO

import requests
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
from skimage.io import imsave

import only_object


class ItemInfo(object):
    def __init__(self, url):
        # set properties
        self.url = url
        self.soup = None
        self.size_info = None
        self.front_img = None
        self.side_img = None
        # initializing method execution
        self.get_soup(timeout=30)

    def get_soup(self, timeout):
        t_start = time.time()
        while time.time() - t_start < timeout:
            r = requests.get(self.url)
            if r.status_code == 200:
                break
        if r.status_code != 200:
            raise ValueError('The url may be invalid')
        self.soup = BeautifulSoup(r.text.encode(r.encoding))
        return self.soup

    def get_size_info(self):
        """size_info = width, depth, height"""
        def scrape_web4size(pattern):
            """scrape the web page corresponding with the each pattern
            in amazon web site"""
            # get elms
            if pattern == 0:
                elms = self.soup.find('div', {'id': 'feature-bullets'})
                if (elms is None) or (len(elms) == 0):
                    return None
                elms = elms.find_all('span', {'class': 'a-list-item'})
            elif pattern == 1:
                elms = self.soup.find_all('tr', {'class': 'size-weight'})
            # scrape size with shared way
            if len(elms) == 0:
                return None
            size_texts = [elm.get_text() for elm in elms if u'cm' in elm.get_text()]
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
            # for just there is radius
            if len(size_info) == 2:
                size_info.append(size_info[0])
            return size_info
        # try each pattern
        for i in range(2):
            size_info = scrape_web4size(pattern=i)
            if size_info is not None:
                self.size_info = size_info
                return self.size_info

    def get_item_img(self):
        elm = self.soup.find('img', {'id': 'landingImage'})
        imgs = eval(elm.get('data-a-dynamic-image'))
        # get largest img
        img_url = sorted([(h*w, url) for url, (h, w) in imgs.items()])[-1][1]

        # download & load img as numpy.array
        r = requests.get(img_url)
        img = np.asarray(Image.open(StringIO(r.content)))

        front = only_object.only_object(img)
        # other side color
        color = front.mean(axis=0).mean(axis=0)
        side_img = np.zeros_like(front)
        side_img[:] = color
        # save img
        self.front_img = front
        self.side_img = side_img

        return self.front_img, self.side_img

    def predict_correct_size_info(self):
        """size_info = width, depth, height"""
        if self.front_img is None:
            self.get_item_img()
        if self.size_info is None:
            self.get_size_info()
        height, width, _ = self.front_img.shape
        img_scaled_area = 1. * height / width * width
        s1, s2, s3 = self.size_info
        s1, s2, s3 = 1., 1.*s2/s1, 1.*s3/s1
        scaled_areas = np.array([s1*s2, s2*s3, s3*s1])
        depth_index = -1 + np.argmin(np.abs(scaled_areas - img_scaled_area))
        depth = self.size_info.pop(depth_index)
        self.size_info.insert(1, depth)
        return self.size_info


def main(url):
    item_info = ItemInfo(url=url)
    size_info = item_info.get_size_info()
    front, side = item_info.get_item_img()
    size_info = item_info.predict_correct_size_info()

    # save imgs
    img_nm = hashlib.md5(url).hexdigest()
    fpath = os.path.dirname(os.path.abspath(__file__))
    imsave(fpath + '/item_img/{0}_front.png'.format(img_nm), front)
    front_upside_down = front[::-1, :].copy()
    imsave(fpath + '/item_img/{0}_front_upside_down.png'.format(img_nm), front_upside_down)
    imsave(fpath + '/item_img/{0}_side.png'.format(img_nm), side)
    with open(fpath + '/item_img/{0}_size.csv'.format(img_nm), 'w') as f:
        f.write(','.join(map(str, size_info)))


if __name__ == '__main__':
    url = 'http://www.amazon.co.jp/%E4%B8%8D%E4%BA%8C%E8%B2%BF%E6%98%93-%E3%83%95%E3%83%AA%E3%83%BC%E3%83%9C%E3%83%83%E3%82%AF%E3%82%B9-FBC960-%E3%82%AB%E3%83%A9%E3%83%BC%E3%83%9C%E3%83%83%E3%82%AF%E3%82%B9-57093/dp/B00163JL6E/ref=sr_1_3?s=home&ie=UTF8&qid=1418455551&sr=1-3&keywords=%E6%A3%9A'
    main(url)