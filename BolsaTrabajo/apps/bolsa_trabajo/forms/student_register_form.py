#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class StudentRegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 80, label = 'Primer nombre')
    last_name = forms.CharField(max_length = 80, label = 'Apellido paterno')
    email = forms.EmailField(max_length = 80, label = 'Correo electrónico')
    level = forms.ModelChoiceField(queryset = StudentLevel.objects.all(), label = 'Nivel')
    resume = forms.CharField(widget = forms.Textarea(), label = 'Resumen de tu perfil')
    username = forms.CharField(max_length = 80, label = 'Nombre de usuario para ingresar al sistema')
    password = forms.CharField(max_length = 80, label = 'Contraseña', widget = forms.PasswordInput())
    repeat_password = forms.CharField(max_length = 80, label = 'Repita la contraseña', widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data['password']
        repeat_password = cleaned_data['repeat_password']
        if password != repeat_password:
            raise ValidationError('Las contraseñas deben ser iguales')

        return cleaned_data
