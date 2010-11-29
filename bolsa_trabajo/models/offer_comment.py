#-*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import EnterpriseCommentRing, Student, Offer

class OfferComment(models.Model):
    Offer = models.ForeignKey(Offer)
    author = models.ForeignKey(User)
    body = models.TextField()
    parent = models.ForeignKey('self', null = True)
    new_replies = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add = True)
    
    def clear(self):
        # Verificar que el autor es estudiante o la empresa original
        if not isinstance(self.author, Student) and self.author != self.Offer.enterprise:
            raise ValidationError('Terceras empresas no pueden comentar sobre otras empresas')

    def __unicode__(self):
        return unicode(self.Offer) + ' - ' + unicode(self.author)
    
    class Meta:
        app_label = 'bolsa_trabajo'
