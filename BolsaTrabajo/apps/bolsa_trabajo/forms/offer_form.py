#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class OfferForm(forms.Form):
    title = forms.CharField(label = 'Título')
    description = forms.CharField(widget = forms.Textarea(), label = 'Descripción del trabajo')
    liquid_salary = forms.IntegerField(label = 'Sueldo líquido (0 si se requiere pretensión de salario)')
    available_slots = forms.IntegerField(label = 'Número de puestos disponibles (0 si son indeterminados)')
    level = forms.ModelMultipleChoiceField(queryset = OfferLevel.objects.all(), label = 'Nivel (puede seleccionar más de uno manteniendo apretada la tecla Control)', required = True)
    tags = forms.CharField(label = 'Palabras clave separadas por coma (e.g. "MySQL, CakePHP")', required = True)
    
    @staticmethod
    def create_from_offer(offer):
        form = OfferForm()
        form.fields['title'].initial = offer.title
        form.fields['description'].initial = offer.description
        form.fields['liquid_salary'].initial = offer.liquid_salary
        form.fields['available_slots'].initial = offer.available_slots
        form.fields['level'].initial = [level.id for level in offer.level.all()]
        form.fields['tags'].initial = ', '.join([tag.name for tag in offer.tags.all()])
        return form
