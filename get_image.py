#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import sys

def get_image(url):
    url =
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode(r.encoding))
    spans = soup.find("div", {"class": "stream-media-grid-items media-grid"}).findAll("span")
    for span in spans:
        img_url = span.get("data-resolved-url-large")
        if img_url is None:
            continue

        os.system('wget  -q {0} -P {1} -O {2}'.format(img_url, "./bbb", os.path.basename(img_url).rstrip(":large") + "g"))

if __name__ == '__main__':
    url = sys.argv[1]
    get_image(url)
