# from django.db import models
from django import forms

# Create your models here.
# class Greeting(models.Model):
    # when = models.DateTimeField('date created', auto_now_add=True)

class IndexForm(forms.Form):
    amazon_item_url = forms.CharField(max_length=1000)
    marker_size = forms.CharField(max_length=100)
