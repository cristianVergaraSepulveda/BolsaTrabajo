#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import OfferMessageRing


class OfferMessage(models.Model):
    ring = models.ForeignKey(OfferMessageRing)
    author = models.ForeignKey(User)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def clear(self):
        # Verificar que al autor es o el estudiante o la empresa
        if self.author != self.ring.author and self.author != self.ring.Offer.enterprise:
            raise ValidationError('El mensaje debe ser emitido por una de las dos partes')

    def __unicode__(self):
        return unicode(self.ring) + ' - ' + unicode(self.author)

    class Meta:
        app_label = 'bolsa_trabajo'
