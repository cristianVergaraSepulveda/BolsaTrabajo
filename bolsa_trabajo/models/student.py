#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q

class Student(User):
    resume = models.TextField()
    has_cv = models.BooleanField(default = False)

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
