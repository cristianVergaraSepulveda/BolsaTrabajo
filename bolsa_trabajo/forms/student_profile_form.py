#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class StudentProfileForm(forms.Form):
    resume = forms.CharField(widget = forms.Textarea(), label = 'Resumen de tu perfil')
    block_public_access = forms.BooleanField(label = '¿Bloquear acceso público?')
    cv = forms.FileField(label = 'Currículum Vitae (PDF)', required = False)
    
    @staticmethod
    def new_from_student(student):
        form = StudentProfileForm()
        form.fields['resume'].initial = student.resume
        form.fields['block_public_access'].initial = student.profile.block_public_access
        
        return form
