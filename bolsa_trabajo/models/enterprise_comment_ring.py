#-*- coding: UTF-8 -*-
from django.db import models
from bolsa_trabajo.models import Enterprise

class EnterpriseCommentRing(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    title = models.CharField(max_length = 255)
    last_change = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return unicode(self.enterprise) + ' - ' + unicode(self.title)
    
    class Meta:
        app_label = 'bolsa_trabajo'
