#-*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import *
from bolsa_trabajo.models.offer import *

class OfferStatusForm(forms.Form):

    closure_reason = forms.ChoiceField(choices = Offer.CLOSURE_REASON_CHOICES, label = 'Razón por la que se cerró la oferta')

    @staticmethod
    def create_from_offer(offer):
        form = OfferStatusForm()
        form.fields['closure_reason'].initial = offer.closure_reason
        return form
