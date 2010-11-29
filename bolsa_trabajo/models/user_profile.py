#-*- coding: UTF-8 -*-
import hashlib
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from bolsa_trabajo.models import Tag
from bolsa_trabajo.models import Student, Enterprise
from django.template.loader import get_template
from bolsa_trabajo.utils import *
import settings

class UserProfile(models.Model):
    validated_email = models.BooleanField(default = False)
    user = models.OneToOneField(User, related_name = 'profile')
    tags = models.ManyToManyField(Tag, blank = True, null = True)
    block_public_access = models.BooleanField(default = False)   

    def __unicode__(self):  
        return 'Perfil de %s' % self.user
        
    class Meta:
        app_label = 'bolsa_trabajo'
        
    @staticmethod
    def notify_staff_of_new_register():
        users = User.objects.filter(is_staff = True).filter(is_superuser = False)
        for user in users:
            user.profile.send_new_register_mail()
            
    def send_new_register_mail(self):
        subject = 'Bolsa de Trabajo - Nueva empresa solicita autorización'

        t = get_template('mails/new_enterprise_request.html')

        send_email(self.user, subject, t, {})
        
    def send_register_mail(self):
        self.send_confirmation_mail_from_template('mails/confirmation_mail.html')
        
    def send_change_mail_confirmation(self):
        self.send_confirmation_mail_from_template('mails/change_mail.html')    
        
    def send_confirmation_mail_from_template(self, template):
        subject = 'Bolsa de Trabajo - Confirmación de correo electrónico'
        user_digest = hashlib.sha224(settings.SECRET_KEY + self.user.username + self.user.email).hexdigest()

        t = get_template(template)
        args = {'user_digest': user_digest}

        send_email(self.user, subject, t, args)
        
    def error_list(self):
        if self.is_student():
            return ''
        elif self.is_enterprise():
            return 'Enterprise'
        else:
            raise Exception
        
    def is_student(self):
        students = Student.objects.filter(pk = self.user.id)
        if students:
            return True
        else:
            return False
            
    def is_enterprise(self):
        enterprises = Enterprise.objects.filter(pk = self.user.id)
        if enterprises:
            return True
        else:
            return False

def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        profile, created = UserProfile.objects.get_or_create(user = instance)

post_save.connect(create_user_profile, sender = User) 
post_save.connect(create_user_profile, sender = Student) 
post_save.connect(create_user_profile, sender = Enterprise) 
