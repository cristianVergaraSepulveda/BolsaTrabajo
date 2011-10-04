#-*- coding: utf-8 -*-

import os

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.loader import get_template

from . import Tag
from . import StudentLevel
from ..email import send_email


class Student(User):
    resume = models.TextField()
    has_cv = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    level = models.ForeignKey(StudentLevel)

    def get_tags_string(self):
        tags = self.tags.all()
        return ', '.join(tag.name for tag in tags)

    def get_resume_string(self):
        suffix = ''
        if len(self.resume) > 300:
            suffix = ' ...'
        return self.resume[:300] + suffix

    @staticmethod
    def get_from_form(form, include_hidden):
        from . import UserProfile
        #students = Student.objects.filter(is_active = True).filter(profile__block_public_access = False)
        profiles = [p.user.id for p in UserProfile.objects.filter(approved=True, block_public_access=False)]
        students = Student.objects.filter(id__in=profiles)

        if form.is_valid():
            data = form.cleaned_data
            if not data['include_unavailable_cv']:
                students = students.filter(has_cv=True)
            if data['level']:
                students = students.filter(level__in=data['level']).distinct()
            if data['tags']:
                tags = Tag.parse_string(data['tags'])
                if tags:
                    students = students.filter(tags__in=tags).distinct()
                    for student in students:
                        student.affinity = student.get_affinity(tags)
                    students = sorted(students, key=lambda student: student.affinity, reverse=True)
                valid_tags_string = ', '.join([tag.name for tag in tags])

                copied_data = form.data.copy()
                copied_data['tags'] = valid_tags_string
                form.data = copied_data

        for student in students:
            if not 'affinity' in dir(student):
                student.affinity = 0
        return students

    def get_affinity(self, tags):
        if not tags:
            return None
        num_tags = len(tags)
        num_hits = 0
        for tag in tags:
            if tag in self.tags.all():
                num_hits += 1

        return int(100 * num_hits / num_tags)

    def update_from_form(self, form):
        self.resume = form.cleaned_data['resume']
        self.level = form.cleaned_data['level']
        self.profile.block_public_access = form.cleaned_data['block_public_access']
        if 'cv' in form.cleaned_data and form.cleaned_data['cv']:
            self.has_cv = True
            self.store_cv(form.cleaned_data['cv'])
        tags = Tag.parse_string(form.cleaned_data['tags'], True)
        self.tags.clear()
        for tag in tags:
            self.tags.add(tag)

    def store_cv(self, uploaded_file):
        filename = uploaded_file.name

        (file_name, extension) = os.path.splitext(filename)

        print filename
        print file_name
        print extension
        if extension.lower() != '.pdf':
            raise Exception('Por favor seleccione un archivo PDF')

        destination = open(os.path.join(settings.DJANGO_ROOT, 'media/cv/%d.pdf' % self.id), 'wb+')
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
        destination.close()

    def delete_cv(self):
        self.has_cv = False
        try:
            filename = os.path.join(settings.DJANGO_ROOT, 'media/cv/%d.pdf' % self.id)
            print filename
            os.remove(filename)
        except:
            pass

    def notify_acceptance(self):
        t = get_template('mails/student_acceptance.html')
        subject = '[Bolsa Trabajo CaDCC] Solicitud de Registro Aceptada'

        send_email(self, subject, t, {})

    def notify_rejection(self):
        t = get_template('mails/user_rejection.html')
        subject = '[Bolsa Trabajo CaDCC] Solicitud de Registro Rechazada'

        send_email(self, subject, t, {})

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
        #student.is_active = False
        student.level = data['level']
        return student

    @staticmethod
    def get_pending_requests():
        #return Enterprise.objects.filter(is_active = False).filter(profile__validated_email = True)
        #return Student.objects.filter(profile__accepted = False).filter(profile__validated_email = True)
        #return Enterprise.objects.filter(profile__approved = False).filter(profile__validated_email = True)
        return Student.objects.filter(profile__validated_email=True).filter(profile__approved=False)

    def save(self):
        same_username_users = User.objects.filter(username=self.username).filter(~Q(pk=self.id))
        if same_username_users:
            raise ValidationError('')
        super(Student, self).save()

    def is_postulating_to(self, offer):
        from .postulation import Postulation
        try:
            Postulation.objects.get(student=self, offer=offer)
        except Postulation.DoesNotExist:
            return False
        return True

    def has_open_postulations_with(self, enterprise):
        from .postulation import Postulation
        postulations = Postulation.objects.filter(student=self, status=Postulation.OPEN_POSTULATION, offer__enterprise=enterprise)
        return bool(postulations)

    class Meta:
        app_label = 'bolsa_trabajo'
