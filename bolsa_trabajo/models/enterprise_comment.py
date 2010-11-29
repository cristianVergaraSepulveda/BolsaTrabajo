#-*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import EnterpriseCommentRing, Student

class EnterpriseComment(models.Model):
    ring = models.ForeignKey(EnterpriseCommentRing)
    author = models.ForeignKey(User)
    body = models.TextField()
    parent = models.ForeignKey('self', null = True)
    unread_replies = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add = True)
    
    def clear(self):
        # Verificar que el padre pertenezca al mismo anillo
        if self.parent and self.parent.ring != self.ring:
            raise ValidationError('El anillo de mensajes del padre debe ser igual al propio')
            
        # Verificar que el autor es estudiante o la empresa original
        if not isinstance(self.author, Student) and self.author != self.ring.enterprise:
            raise ValidationError('Terceras empresas no pueden comentar sobre otras empresas')

    def __unicode__(self):
        return unicode(self.ring) + ' - ' + unicode(self.author)
    
    class Meta:
        app_label = 'bolsa_trabajo'
