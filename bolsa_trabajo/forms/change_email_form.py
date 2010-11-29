#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError

class ChangeEmailForm(forms.Form):
    password = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput)
    new_email = forms.CharField(label = 'Nuevo correo electrónico')
