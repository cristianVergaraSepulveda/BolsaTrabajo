#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class EnterpriseProfileForm(forms.Form):
    phone = forms.CharField(label = 'Teléfono')
    address = forms.CharField(label = 'Dirección')
    website = forms.CharField(label = 'Sitio web')
    description = forms.CharField(widget = forms.Textarea(), label = 'Descripción de la empresa')
    block_public_access = forms.BooleanField(label = '¿Bloquear acceso público?', required = False)
    
    @staticmethod
    def new_from_enterprise(enterprise):
        form = EnterpriseProfileForm()
        form.fields['phone'].initial = enterprise.phone
        form.fields['address'].initial = enterprise.address
        form.fields['website'].initial = enterprise.website
        form.fields['description'].initial = enterprise.description
        form.fields['block_public_access'].initial = enterprise.profile.block_public_access
        
        return form
