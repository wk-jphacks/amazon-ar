#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import sys

import yaml
import bottlenose
from bs4 import BeautifulSoup


def get_api_key():
    dirpath = os.path.dirname(os.path.abspath(__file__))
    api_config_fname = os.path.join(dirpath, '../config/amazon_api.yml')
    with open(api_config_fname, 'rb') as f:
        data = yaml.load(f)
        api_key = data['amazon_api_key']
    return api_key


def get_item_dimensions(item_id, amazon):
    """Get item dimensions from api response xml."""
    response = amazon.ItemLookup(ItemId=item_id,
        ResponseGroup='ItemAttributes')
    item_dims = response.find('itemdimensions')
    item_dims = map(lambda x:float(x.text),
        [item_dims.height, item_dims.width, item_dims.length])
    item_dims = dict(zip(['height', 'width', 'length'], item_dims))
    return item_dims


def get_item_img_url(item_id, amazon):
    """Get item img url from api response xml."""
    response = amazon.ItemLookup(ItemId=item_id, ResponseGroup='Images')
    img_url = response.find('largeimage').url.text
    return img_url


def main():
    api_key = get_api_key()
    amazon = bottlenose.Amazon(
        AWSAccessKeyId=api_key['access_key_id'],
        AWSSecretAccessKey=api_key['secret_access_key'],
        AssociateTag='wkentaro-22',
        Region='JP',
        Parser=BeautifulSoup,
        )

    # get item_id from url
    if len(sys.argv) == 1:
        url = "http://www.amazon.co.jp/REVOLTECH-DANBOARD-mini-cheero-ver-%E3%83%AA%E3%83%9C%E3%83%AB%E3%83%86%E3%83%83%E3%82%AF/dp/B00HVTABES/ref=pd_sim_hb_5?ie=UTF8&refRID=1YQ9X8XS4FCTD1Z7A8BB"
    else:
        url = sys.argv[1]
    url_nodes = url.split('/')
    item_id = url_nodes[url_nodes.index('dp') + 1]

    # get item dimensions
    item_dims = get_item_dimensions(item_id, amazon)
    print(item_dims)

    # get item img
    item_url = get_item_img_url(item_id, amazon)
    print(item_url)


if __name__ == '__main__':
    main()

