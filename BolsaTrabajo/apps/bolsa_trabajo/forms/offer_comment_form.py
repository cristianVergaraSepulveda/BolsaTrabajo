#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class OfferCommentForm(forms.Form):
    parent = forms.ModelChoiceField(queryset = OfferComment.objects.all(), required = False)
    body = forms.CharField(widget = forms.Textarea())
