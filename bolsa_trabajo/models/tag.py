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
            
    @staticmethod
    def parse_string(string):
        tag_names = [name.strip() for name in string.split(',')]
        tags = set()
        for tag_name in tag_names:
            if not tag_name:
                continue
            try:
                tag = Tag.objects.get(name__iexact = tag_name)
            except:
                tag = Tag()
                tag.name = tag_name
                tag.save()
            tags.add(tag)
        return list(tags)

    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        app_label = 'bolsa_trabajo'
        ordering = ('name',)
