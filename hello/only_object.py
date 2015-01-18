#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Get only object in a image by making
the white background transparent.
"""


__author__ = 'www.kentaro.wada@gmail.com (Kentaro Wada)'


import numpy as np
from PIL import Image

from skimage.color import gray2rgb, rgb2gray
from skimage.filter import threshold_otsu
from skimage import morphology
from skimage.morphology import closing
from skimage import measure
from skimage.measure import regionprops
from skimage.restoration import denoise_tv_chambolle


def is_gray(img):
    """Check the img array is gray"""
    return len(img.shape) == 2


def rgb2rgba(img):
    """convert RGB img array to RGBA"""
    img_pil_rgb = Image.fromarray(img)
    img_pil_rgba = img_pil_rgb.convert('RGBA')
    img_rgba = np.asarray(img_pil_rgba)
    img_rgba.setflags(write=True)
    return img_rgba


def make_white_bg_transparent(img):
    """Make white background transparent"""
    if len(img.shape) == 2:
        img = gray2rgb(img)
    img_rgba = rgb2rgba(img)
    # get threshold
    color_map = img_rgba.sum(axis=-1)
    thresh = (color_map.max() - color_map.mean()) * 4. / 5.
    thresh += color_map.mean()
    # make transparent
    img_rgba[img_rgba.sum(axis=-1) > thresh] = [255, 255, 255, 0]
    return img_rgba


def crop_biggest_object(img):
    """Crop biggest object in the img"""
    img_origin = img.copy()
    if is_gray(img):
        imgray = img
    else:
        imgray = rgb2gray(img)
    img_denoised = denoise_tv_chambolle(imgray, weight=.1)
    thresh = threshold_otsu(img_denoised)
    # get label_img
    bw = closing(img_denoised > thresh, morphology.square(2))
    cleared = bw.copy()
    label_img = measure.label(cleared)
    borders = np.logical_xor(bw, cleared)
    label_img[borders] = -1
    # get biggest area
    max_region = sorted((region.area, region)
        for region in regionprops(label_img))[-1][1]
    minr, minc, maxr, maxc = max_region.bbox
    return img_origin[minr:maxr, minc:maxc]


def only_object(img):
    """Get only object RGBA by making backgroun transparent"""
    cropped = crop_biggest_object(img)
    only_object = make_white_bg_transparent(cropped)
    return only_object


def main():
    import StringIO
    import requests
    import matplotlib.pyplot as plt
    from skimage.io import imsave
    url = "http://ecx.images-amazon.com/images/I/51%2BWhA0AofL._SX522_.jpg"
    res = requests.get(url)
    img = np.asarray(Image.open(StringIO.StringIO(res.content)))
    img_only_object = only_object(img)
    imsave('original.png', img)
    imsave('only_object.png', img_only_object)


if __name__ == '__main__':
    main()
