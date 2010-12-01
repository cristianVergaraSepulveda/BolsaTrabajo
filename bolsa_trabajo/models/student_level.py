#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError

class StudentLevel(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    ordering = models.IntegerField() 
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = 'bolsa_trabajo'
        ordering = ('ordering',)
