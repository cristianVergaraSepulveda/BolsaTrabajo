#-*- coding: utf-8 -*-

from django.db import models


class OfferLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    minimum_salary = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        app_label = 'bolsa_trabajo'
        ordering = ('name',)
