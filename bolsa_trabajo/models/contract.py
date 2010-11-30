#-*- coding: UTF-8 -*-
from django.db import models
from bolsa_trabajo.models import Application, ContractFeedback

class Contract(models.Model):
    application = models.ForeignKey(Application)
    student_feedback = models.OneToOneField(ContractFeedback, related_name = 'student_contract')
    enterprise_feedback = models.OneToOneField(ContractFeedback, related_name = 'enterprise_contract')
    start_date = models.DateField()
    end_date = models.DateField()
    enterprise = property(lambda self: self.application.enterprise)
    student = property(lambda self: self.application.student)
    offer = property(lambda self: self.application.message.offer)
    
    def __unicode__(self):
        return unicode(self.enterprise) + ' - ' + unicode(self.student)
    
    class Meta:
        app_label = 'bolsa_trabajo'
