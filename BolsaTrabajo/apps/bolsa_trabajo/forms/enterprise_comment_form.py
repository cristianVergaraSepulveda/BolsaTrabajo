#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class EnterpriseCommentForm(forms.Form):
    parent = forms.ModelChoiceField(queryset = EnterpriseComment.objects.all(), required = False)
    body = forms.CharField(widget = forms.Textarea())
