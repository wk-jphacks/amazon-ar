#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import sys


def get_product_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode(r.encoding))


if __name__ == '__main__':
    url = sys.argv[1]
    get_product_info(url)

