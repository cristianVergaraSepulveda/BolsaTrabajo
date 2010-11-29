#-*- coding: UTF-8 -*-
from django.db import models
from bolsa_trabajo.models import OfferMessageRing

class Application(models.Model):
    message = models.ForeignKey(OfferMessageRing)
    enterprise = property(lambda self: self.message.offer.enterprise)
    student = property(lambda self: self.message.student)
    
    def __unicode__(self):
        return unicode(self.enterprise) + ' - ' + unicode(self.student)
    
    class Meta:
        app_label = 'bolsa_trabajo'
