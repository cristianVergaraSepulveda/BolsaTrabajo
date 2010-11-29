#-*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from bolsa_trabajo.models import ContractFeedbackEvaluation

class ContractFeedback(models.Model):
    evaluation = models.ForeignKey(ContractFeedbackEvaluation)
    comments = models.TextField()
    creation_date = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return unicode(self.enterprise) + ' - ' + unicode(self.title)
    
    class Meta:
        app_label = 'bolsa_trabajo'
