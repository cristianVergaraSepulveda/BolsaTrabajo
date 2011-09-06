#-*- coding: utf-8 -*-

from django.db.models import Q
from django.db import models
from django.template.loader import get_template

from . import Tag
from . import Enterprise
from . import OfferLevel
from .utils import get_delta
from .utils import pretty_price
from ..email import send_email


class Postulation(models.Model):

    STATUS_OPTIONS = (
        (1,'Abierta'),
        (2,'Cerrada sin contratar'),
        (3,'Cerrada y contratado')
    )

    status = models.IntegerField(choices=STATUS_OPTIONS, default=1)
    offer = models.ForeignKey('Offer')
    student = models.ForeignKey('Student')
    is_closed = models.BooleanField(default=False)

    class Meta:
        app_label = 'bolsa_trabajo'
        unique_together = ("offer", "student")
