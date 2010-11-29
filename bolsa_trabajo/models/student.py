#-*- coding: UTF-8 -*-
import os
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q
import settings


class Student(User):
    resume = models.TextField()
    has_cv = models.BooleanField(default = False)
    
    def update_from_form(self, form):
        self.resume = form.cleaned_data['resume']
        self.profile.block_public_access = form.cleaned_data['block_public_access']
        if 'cv' in form.cleaned_data and form.cleaned_data['cv']:
            self.has_cv = True
            self.store_cv(form.cleaned_data['cv'])
    
    def store_cv(self, uploaded_file):
        filename = uploaded_file.name
        
        (file_name, extension) = os.path.splitext(filename)        
        
        print filename
        print file_name
        print extension
        if extension.lower() != '.pdf':
            raise Exception('Por favor seleccione un archivo PDF')
        
        destination = open(os.path.join(settings.PROJECT_ROOT, 'media/cv/%d.pdf' % self.id), 'wb+')
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
        destination.close()
        
    def delete_cv(self):
        self.has_cv = False
        try:
            filename = os.path.join(settings.PROJECT_ROOT, 'media/cv/%d.pdf' % self.id)
            print filename
            os.remove(filename)
        except:
            pass

    @staticmethod
    def create_from_form(form):
        data = form.cleaned_data
        student = Student()
        student.resume = data['resume']
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.username = data['username']
        student.email = data['email']
        student.set_password(data['password'])
        student.is_active = False
        return student
        
    def save(self):
        same_username_users = User.objects.filter(username = self.username).filter(~Q(pk = self.id))
        if same_username_users:
            raise ValidationError('')
        super(Student, self).save()

    class Meta:
        app_label = 'bolsa_trabajo'
