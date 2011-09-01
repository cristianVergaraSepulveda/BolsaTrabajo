#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class StudentProfileForm(forms.Form):
    resume = forms.CharField(widget = forms.Textarea(), label = 'Resumen de tu perfil')
    level = forms.ModelChoiceField(queryset = StudentLevel.objects.all(), label = 'Nivel')
    block_public_access = forms.BooleanField(label = '¿Bloquear acceso y búsquedas de tu perfil?', required = False)
    cv = forms.FileField(label = 'Currículum Vitae (PDF)', required = False)
    tags = forms.CharField(label = 'Habilidades clave separadas por coma (e.g. "MySQL, CakePHP")', required = False)
    
    @staticmethod
    def new_from_student(student):
        form = StudentProfileForm()
        form.fields['level'].initial = student.level.id
        form.fields['resume'].initial = student.resume
        form.fields['block_public_access'].initial = student.profile.block_public_access
        form.fields['tags'].initial = ', '.join([tag.name for tag in student.tags.all()])
        
        return form
