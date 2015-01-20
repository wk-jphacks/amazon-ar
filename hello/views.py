from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import IndexForm
import item_info

import requests
import hashlib
import os
import qrcode


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['amazon_item_url']
            marker_size = int(float(form.cleaned_data['marker_size']) * 10)
            size_info = item_info.main(url)
            if size_info is not None:
                width, height, depth = item_info.main(url)
            else:
                width, height, depth = 0, 0, 0
            img_name = hashlib.md5(url.encode('utf-8')).hexdigest()
            redirect_url = '/ar/?msize={0}&img={1}&width={2}&height={3}&depth={4}'.format(marker_size, img_name, width, height, depth)
            img_qrcode = qrcode.make('http://{0}{1}'.format(request.META.get('HTTP_HOST', ''), redirect_url))
            fpath = os.path.dirname(os.path.abspath(__file__))
            img_qrcode.save('{}/item_img/{}_qr.png'.format(fpath, img_name))
            return HttpResponseRedirect(redirect_url)
    else: # if 'GET'
        form = IndexForm()

    return render(request, 'index.html', {'form': form})


def ar(request):
    return render(request, 'ar.html')

# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, 'db.html', {'greetings': greetings})

