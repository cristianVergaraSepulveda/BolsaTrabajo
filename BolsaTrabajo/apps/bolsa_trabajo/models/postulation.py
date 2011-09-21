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

    OPEN_POSTULATION=1
    status = models.IntegerField(choices=STATUS_OPTIONS, default=1)
    offer = models.ForeignKey('Offer')
    student = models.ForeignKey('Student')

    def close(self, student_hired):
        if not student_hired:
            self.status = 2
            self.notify_rejection()
        else:
            self.status = 3
            self.notify_hired()
            from . import WorkRegistry
            work_registry = WorkRegistry(postulation=self)
            work_registry.save()
            if not self.offer.is_closed() and not self.offer.has_available_slots():
                self.offer.close_by_full_slots()
        self.save()

    def notify_rejection(self):
        t = get_template('mails/notify_rejected_postulation.html')
        subject = u'[Bolsa Trabajo CaDCC] Tu postulación ha sido cerrada'
        send_email(self.student, subject, t, {'postulation': self})

    def notify_hired(self):
        t = get_template('mails/notify_hired_postulation.html')
        subject = u'[Bolsa Trabajo CaDCC] Has sido aceptado para la oferta %s' % unicode(self.offer)
        send_email(self.student, subject, t, {'postulation': self})

    def is_closed(self):
        if self.status == 2 or self.status == 3:
            return True
        else:
            return False

    class Meta:
        app_label = 'bolsa_trabajo'
        unique_together = ("offer", "student")
