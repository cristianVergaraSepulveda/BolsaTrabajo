#-*- coding: utf-8 -*-

from django.db.models import Q
from django.db import models
from django.template.loader import get_template

from . import Postulation

class WorkRegistry(models.Model):

    postulation = models.ForeignKey('Postulation')

    def accept_student(self):
        self.is_closed = True
        


    class Meta:
        app_label = 'bolsa_trabajo'