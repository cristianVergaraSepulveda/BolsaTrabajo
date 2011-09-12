#-*- coding: UTF-8 -*-

from django import forms
from bolsa_trabajo.models import Offer


class OfferStatusForm(forms.Form):

    closure_reason = forms.ChoiceField(choices = Offer.CLOSURE_REASON_CHOICES[:-1], label = 'Razón de cierre de la oferta')

    @staticmethod
    def create_from_offer(offer):
        form = OfferStatusForm()
        form.fields['closure_reason'].initial = offer.closure_reason
        return form
