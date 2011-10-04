#-*- coding: utf-8 -*-

import datetime

from django.db.models import Q
from django.db import models
from django.template.loader import get_template
from django.contrib.auth.models import User

from . import Tag
from . import OfferLevel
from .utils import get_delta
from .utils import pretty_price
from .utils import now_plus_min_end_date
from ..email import send_email


class Offer(models.Model):

    CLOSURE_REASON_CHOICES = (
        (1, 'Se llenaron los cupos disponibles'),
        (2, 'La oferta de trabajo ya no aplica'),
        (3, 'Cerrada por el administrador'),
    )

    STATUS_CHOICES = (
        (1, 'Pendiente'),
        (2, 'Abierta'),
        (3, 'Cerrada')
    )

    enterprise = models.ForeignKey('Enterprise')
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    liquid_salary = models.IntegerField()
    level = models.ManyToManyField(OfferLevel)
    creation_date = models.DateTimeField(auto_now_add=True)
    available_slots = models.IntegerField()
    has_unread_comments = models.BooleanField(default=False)
    # closure_reason with default value 0 means that the cron system closed
    # the offer due to its expiration date
    closure_reason = models.IntegerField(choices=CLOSURE_REASON_CHOICES, default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    end_date = models.DateField(default=now_plus_min_end_date, blank=False, null=False)

    @classmethod
    def get_closed_without_feedback(self):
        return self.objects.filter(status=3, closure_reason=0)

    @staticmethod
    def create_from_form(enterprise, form):
        data = form.cleaned_data
        offer = Offer()
        offer.enterprise = enterprise
        offer.title = data['title']
        offer.description = data['description']
        offer.liquid_salary = data['liquid_salary']
        offer.available_slots = data['available_slots']
        offer.validated = False
        offer.save()
        tags = Tag.parse_string(data['tags'], True)
        for tag in tags:
            offer.tags.add(tag)
        offer.level = data['level']
        offer.end_date = data['end_date']
        return offer

    def load_from_form(self, form):
        data = form.cleaned_data
        self.title = data['title']
        self.description = data['description']
        self.liquid_salary = data['liquid_salary']
        self.available_slots = data['available_slots']
        tags = Tag.parse_string(data['tags'], True)
        self.tags.clear()
        for tag in tags:
            self.tags.add(tag)
        self.level = data['level']
        self.end_date = data['end_date']

    def change_status_from_form(self, form):
        data = form.cleaned_data
        self.closure_reason = data['closure_reason']

    def is_closed_with_feedback(self):
        return self.is_closed() and self.closure_reason

    def is_closed_without_feedback(self):
        return self.is_closed() and not self.closure_reason

    def is_closed(self):
        return self.status == 3

    def is_closed_by_admin(self):
        return self.is_closed() and self.closure_reason == 3

    def close(self, motive):
        from . import Postulation
        self.status = 3
        self.closure_reason = motive
        self.save()
        for postulation in self.postulation_set.filter(status=Postulation.OPEN_POSTULATION):
            postulation.close(student_hired=False)

    def close_by_admin(self):
        self.close(3)
        self.notify_closed_by_staff()

    def close_by_task(self):
        self.close(0)
        self.notify_expiration()

    def close_by_full_slots(self):
        self.close(1)
        self.notify_full_slots()

    def has_available_slots(self):
        from . import WorkRegistry
        if self.available_slots == 0:
            return True
        elif WorkRegistry.objects.filter(postulation__offer=self).count() < self.available_slots:
            return True
        return False

    def is_pending(self):
        return self.status == 1

    def open(self):
        self.status = 2

    def is_open(self):
        return self.status == 2

    @staticmethod
    def get_pending_requests():
        return Offer.objects.filter(status=1)

    @staticmethod
    def get_unexpired():
        return Offer.objects.filter(status=2)

    @staticmethod
    def get_expired():
        """returns offers with past end_date, but still not closed status"""
        return Offer.objects.filter(status=2).filter(end_date__lt=datetime.date.today)

    @staticmethod
    def get_pendings_feedback_offers(enterpriseId=None):
        if (enterpriseId):
            return Offer.objects.filter(enterprise=enterpriseId, closure_reason=0, status=3)
        return Offer.objects.filter(closure_reason=0, status=3)

    def get_salary_string(self):
        if self.liquid_salary == 0:
            return 'Se requiere enviar pretensión de salario'
        else:
            return pretty_price(self.liquid_salary)

    def get_available_slots_string(self):
        if self.available_slots == 0:
            return 'Puestos indefinidos'
        else:
            return self.available_slots

    def get_level_string(self):
        levels = self.level.all()
        return ', '.join(level.name for level in levels)

    def get_tags_string(self):
        tags = self.tags.all()
        return ', '.join(tag.name for tag in tags)

    def get_description_string(self):
        suffix = ''
        if len(self.description) > 300:
            suffix = ' ...'
        return self.description[:300] + suffix

    @staticmethod
    def get_from_form(form, include_hidden):
        offers = Offer.get_unexpired().filter(status=2).order_by('-creation_date')
        if not include_hidden:
            offers = offers.filter(enterprise__profile__block_public_access=False)

        if form.is_valid():
            data = form.cleaned_data
            if data['enterprise']:
                offers = offers.filter(enterprise=data['enterprise'])
            if data['liquid_salary']:
                #print data['liquid_salary']
                offers = offers.filter(Q(liquid_salary__gte=data['liquid_salary']) | Q(liquid_salary=0))
            if not data['include_unavailable_salaries']:
                offers = offers.filter(liquid_salary__gt=0)
            if data['level']:
                offers = offers.filter(level__in=data['level']).distinct()
            if data['tags']:
                tags = Tag.parse_string(data['tags'])
                if tags:
                    offers = offers.filter(tags__in=tags).distinct()
                    for offer in offers:
                        offer.affinity = offer.get_affinity(tags)
                    offers = sorted(offers, key=lambda offer: offer.affinity, reverse=True)
                valid_tags_string = ', '.join([tag.name for tag in tags])

                copied_data = form.data.copy()
                copied_data['tags'] = valid_tags_string
                form.data = copied_data
        for offer in offers:
            if not 'affinity' in dir(offer):
                offer.affinity = 0

        return offers

    def get_affinity(self, tags):
        if not tags:
            return None
        num_tags = len(tags)
        num_hits = 0
        for tag in tags:
            if tag in self.tags.all():
                num_hits += 1

        return int(100 * num_hits / num_tags)

    def notify_acceptance(self):
        t = get_template('mails/offer_acceptance.html')
        subject = '[Bolsa Trabajo CaDCC] Oferta aceptada'

        send_email(self.enterprise, subject, t, {'offer': self})

    def notify_rejection(self):
        t = get_template('mails/offer_rejection.html')
        subject = '[Bolsa Trabajo CaDCC] Oferta rechazada'

        send_email(self.enterprise, subject, t, {'offer': self})

    def notify_expiration(self):
        t = get_template('mails/offer_expiration_enterprise.html')
        subject = '[Bolsa Trabajo CaDCC] Oferta expirada'
        send_email(self.enterprise, subject, t, {'offer': self})

        t = get_template('mails/offer_expiration_staff.html')
        for user in User.objects.filter(is_staff=True):
            send_email(user, subject, t, {'enterprise': self.enterprise, 'offer': self})

        # t = get_template('mails/offer_expiration_applicant.html')
        # for user in (postulation.student for postulation in self.postulation_set.filter(status=1)):  # only open postulations
        #     send_email(user, subject, t, {'enterprise': self.enterprise, 'offer': self})

    def notify_closed_by_staff(self):
        t = get_template('mails/offer_closed_by_staff.html')
        subject = '[Bolsa Trabajo CaDCC] Oferta cerrada por el staff'
        send_email(self.enterprise, subject, t, {'offer': self})

    def notify_full_slots(self):
        t = get_template('mails/offer_closed_by_full_slots.html')
        subject = '[Bolsa Trabajo CaDCC] Oferta cerrada por cupos llenos'
        send_email(self.enterprise, subject, t, {'offer': self})

    def expired(self):
        return self.creation_date <= get_delta() and self.validated

    def get_closure_reason_name(self):
        if self.closure_reason:
            return self.CLOSURE_REASON_CHOICES[int(self.closure_reason) - 1][1]
        else:
            return u'No se especificó un razón'

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        app_label = 'bolsa_trabajo'
