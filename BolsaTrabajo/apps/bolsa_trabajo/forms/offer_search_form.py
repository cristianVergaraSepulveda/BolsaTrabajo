#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *
from django.utils.http import urlquote

class OfferSearchForm(forms.Form):
    enterprise = forms.ModelChoiceField(queryset = Enterprise.objects.filter(is_active = True), empty_label = 'Cualquiera', required = False, label = 'Empresa')
    level = forms.ModelMultipleChoiceField(queryset = OfferLevel.objects.all(), label = 'Nivel (no seleccione ninguno para incluir todos)', required = False)
    liquid_salary = forms.IntegerField(label = 'Sueldo líquido (0 si quiere mostrar todos)', required = False)
    include_unavailable_salaries = forms.BooleanField(label = '¿Incluir ofertas sin salario (i.e. "Enviar pretensiones de sueldo")?', required = False, initial = True)
    tags = forms.CharField(label = 'Palabras clave separadas por coma (e.g. "MySQL, CakePHP")', required = False)
    page_number = forms.IntegerField(required = False)
    
    def generate_paging_url(self):
        url = '?'
        if self.cleaned_data['enterprise']:
            url += 'enterprise=' + str(self.cleaned_data['enterprise'].id)
        for level in self.cleaned_data['level']:
            url += '&level=%d' % level.id
        if self.cleaned_data['liquid_salary']:
            url += 'liquid_salary=' + str(self.cleaned_data['liquid_salary'])
        if self.cleaned_data['include_unavailable_salaries']:
            url += '&include_unavailable_salaries=on'
        if self.cleaned_data['tags']:
            tags = Tag.parse_string(self.cleaned_data['tags'])
            url += '&tags=' + ', '.join([tag.name for tag in tags])
        return url
