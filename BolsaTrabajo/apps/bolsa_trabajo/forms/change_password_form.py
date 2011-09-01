#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label = 'Contraseña antigua', widget = forms.PasswordInput)
    new_password = forms.CharField(label = 'Nueva contraseña', widget = forms.PasswordInput)
    repeat_new_password = forms.CharField(label = 'Repita la nueva contraseña', widget = forms.PasswordInput)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            password = cleaned_data['new_password']
            repeat_password = cleaned_data['repeat_new_password']
            if password != repeat_password:
                raise ValidationError('Las contraseñas deben ser iguales')
            return cleaned_data
        except ValidationError, e:
            raise ValidationError('Las nuevas contraseñas deben ser iguales')
        except Exception, e:
            raise ValidationError('Por favor ingrese todos los datos')
