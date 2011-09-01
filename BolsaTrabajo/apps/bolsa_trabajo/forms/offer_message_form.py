#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class OfferMessageForm(forms.Form):
    title = forms.CharField(max_length = 255, label = 'Título')
    body = forms.CharField(widget = forms.Textarea(), label = 'Mensaje')
