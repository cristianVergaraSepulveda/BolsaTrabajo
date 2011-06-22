#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *

class OfferStatusForm(forms.Form):
    STATUS_CHOICES = (
        (None,'No se ha establecido una razón'),
        ('Se contrató a más de un postulante utilizando este medio','Se contrató a más de un postulante utilizando este medio'),
        ('Se contrató sólo a un estudiante utilizando este medio','Se contrató sólo a un estudiante utilizando este medio'),
        ('Se contrató sólo postulantes fuera de este medio','Se contrató sólo postulantes fuera de este medio'),
        ('No se ha contratado a nadie','No se ha contratado a nadie'),
    )

    status = forms.ChoiceField(choices = STATUS_CHOICES, label = 'Razón por la que se cerró la oferta')

    @staticmethod
    def create_from_offer(offer):
        form = OfferStatusForm()
        form.fields['status'].initial = offer.status
        return form
