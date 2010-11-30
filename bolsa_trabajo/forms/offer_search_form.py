#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class OfferSearchForm(forms.Form):
    enterprise = forms.ModelChoiceField(queryset = Enterprise.objects.all(), empty_label = 'Cualquiera', required = False, label = 'Empresa')
    level = forms.ModelMultipleChoiceField(queryset = OfferLevel.objects.all(), label = 'Nivel (no seleccione ninguno para incluir todos)', required = False)
    liquid_salary = forms.IntegerField(label = 'Sueldo líquido (0 si quiere mostrar todos)', required = False)
    include_unavailable_salaries = forms.BooleanField(label = '¿Incluir ofertas sin salario (i.e. "Enviar pretensiones de sueldo")?', required = False, initial = True)
    tags = forms.CharField(label = 'Palabras clave separadas por coma (e.g. "MySQL, CakePHP")', required = False)
