#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError

'''
Descripcion de cada "tag" para habilidades técnicas ofrecias
o requeridas (e.g. "MySQL", "CakePHP", etc)
'''
class Tag(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    
    def clean(self):
        # Chequear que no hayan otros tags con el mismo nombre, incluso
        # si varia su uso de mayúsculas.
        name_clashes = Tag.objects.filter(name__iexact = self.name)
        if name_clashes:
            raise ValidationError('No pueden existir dos tags con el mismo nombre')

    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        app_label = 'bolsa_trabajo'
        ordering = ('name',)
