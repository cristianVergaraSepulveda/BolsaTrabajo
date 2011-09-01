#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *
from django.utils.http import urlquote

class StudentSearchForm(forms.Form):
    level = forms.ModelMultipleChoiceField(queryset = StudentLevel.objects.all(), label = 'Nivel (no seleccione ninguno para incluir todos)', required = False)
    include_unavailable_cv = forms.BooleanField(label = '¿Incluir profesionales sin currículum ?', required = False, initial = True)
    tags = forms.CharField(label = 'Palabras clave separadas por coma (e.g. "MySQL, CakePHP")', required = False)
    page_number = forms.IntegerField(required = False)
    
    def generate_paging_url(self):
        url = '?'
        for level in self.cleaned_data['level']:
            url += '&level=%d' % level.id
        if self.cleaned_data['include_unavailable_cv']:
            url += '&include_unavailable_cv=on'
        if self.cleaned_data['tags']:
            tags = Tag.parse_string(self.cleaned_data['tags'])
            url += '&tags=' + ', '.join([tag.name for tag in tags])
        return url
