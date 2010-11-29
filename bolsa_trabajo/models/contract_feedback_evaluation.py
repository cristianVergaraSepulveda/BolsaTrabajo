#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError

class ContractFeedbackEvaluation(models.Model):
    name = models.CharField(max_length = 30)
    ordering = models.IntegerField()

    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        app_label = 'bolsa_trabajo'
        ordering = ('ordering',)
