#!/usr/bin/env python
# -*- coding: utf-8 -*-
# item_info_class.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>
import re
import time
import sha
from StringIO import StringIO

import requests
from bs4 import BeautifulSoup

import numpy as np
from PIL import Image
import cv2


class ItemInfo(object):
    def __init__(self, url):
        # set properties
        self.url = url
        self.soup = None
        self.size_info = None
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
        img = Image.open(StringIO(r.content))
        img = np.array(img)
        img_org = img[:, :, ::-1].copy()

        # get contour
        imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        imgray = cv2.GaussianBlur(imgray, (9, 9), 0)
        ret, thresh = cv2.threshold(imgray, 0, 255,
                cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_with_contours = img.copy()
        cv2.drawContours(img_with_contours, [contours[0]], -1, (0, 255, 0), 1)
        # crop img
        x, y, w, h = cv2.boundingRect(contours[0])
        front = img[y:y+h, x:x+w]
        front = cv2.cvtColor(front, cv2.COLOR_RGB2RGBA)
        front = cv2.cvtColor(front, cv2.COLOR_RGBA2BGRA)
        front[front.sum(axis=-1)>950] = [255,255,255,0]

        # other side color
        color = front.mean(axis=0).mean(axis=0)
        side_img = np.zeros_like(front)
        side_img[:] = color

        # save img
        img_nm = sha.sha(self.url).hexdigest()
        cv2.imwrite('../img/{0}_front.png'.format(img_nm), front)
        cv2.imwrite('../img/{0}_side.png'.format(img_nm), side_img)
        with open('../img/{0}_size.csv'.format(img_nm)) as f:
            f.write(','.join(size_info))

        # debugging
        # cv2.imshow('side', side_img)
        # cv2.imshow('front', front)
        # cv2.imshow('with contours', img_with_contours)
        # cv2.imshow('original', img_org)
        # cv2.waitKey()
        # cv2.destroyAllWindows()


def main():
    item_info = ItemInfo(url='http://www.amazon.co.jp/%E4%B8%8D%E4%BA%8C%E8%B2%BF%E6%98%93-%E3%83%95%E3%83%AA%E3%83%BC%E3%83%9C%E3%83%83%E3%82%AF%E3%82%B9-FBC960-%E3%82%AB%E3%83%A9%E3%83%BC%E3%83%9C%E3%83%83%E3%82%AF%E3%82%B9-57093/dp/B00163JL6E/ref=sr_1_3?s=home&ie=UTF8&qid=1418455551&sr=1-3&keywords=%E6%A3%9A')
    item_info.get_item_img()
    item_info.get_size_info()


if __name__ == '__main__':
    main()