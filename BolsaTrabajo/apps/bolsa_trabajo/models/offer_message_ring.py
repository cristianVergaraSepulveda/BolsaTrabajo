#-*- coding: utf-8 -*-

from django.db import models

from . import Offer
from . import Student


class OfferMessageRing(models.Model):
    offer = models.ForeignKey(Offer)
    student = models.ForeignKey(Student)
    title = models.CharField(max_length=255)
    last_change = models.DateTimeField(auto_now_add=True)
    unread_messages = models.IntegerField()

    def __unicode__(self):
        return unicode(self.Offer) + ' - ' + unicode(self.author)

    class Meta:
        app_label = 'bolsa_trabajo'
