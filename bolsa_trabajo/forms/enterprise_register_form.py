#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class EnterpriseRegisterForm(forms.Form):
    name = forms.CharField(max_length = 255, label = 'Nombre')
    rut = forms.CharField(max_length = 20, label = 'RUT')
    phone = forms.CharField(max_length = 30, label = 'Teléfono')
    address = forms.CharField(max_length = 80, label = 'Dirección')
    website = forms.CharField(max_length = 80, label = 'Sitio web')
    description = forms.CharField(widget = forms.Textarea(), label = 'Descripción de la empresa')
    first_name = forms.CharField(max_length = 80, label = 'Primer nombre')
    last_name = forms.CharField(max_length = 80, label = 'Apellido paterno')
    email = forms.EmailField(max_length = 80, label = 'Correo electrónico')
    username = forms.CharField(max_length = 80, label = 'Nombre de usuario para ingresar al sistema')
    password = forms.CharField(max_length = 80, label = 'Contraseña', widget = forms.PasswordInput())
    repeat_password = forms.CharField(max_length = 80, label = 'Repita la contraseña', widget = forms.PasswordInput())
    
    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            password = cleaned_data['password']
            repeat_password = cleaned_data['repeat_password']
            if password != repeat_password:
                raise ValidationError('Las contraseñas deben ser iguales')
            
            return cleaned_data
        except:
            raise ValidationError('Por favor ingrese los datos solicitados')
