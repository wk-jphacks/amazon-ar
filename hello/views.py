from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import item_info

import requests


# Create your views here.
def index(request):
    return render(request, 'index.html')

def get_item_info(request):
    item_info.main(url)

def ar(request):
    return HttpResponse('Hello AR')

# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, 'db.html', {'greetings': greetings})

