#-*- coding: UTF-8 -*-

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.loader import get_template

from ..email import send_email


class Enterprise(User):
    name = models.CharField(max_length=255)
    rut = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=80)
    website = models.CharField(max_length=80)
    description = models.TextField()
    has_unread_comments = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def notify_acceptance(self):
        t = get_template('mails/enterprise_acceptance.html')
        subject = '[Bolsa Trabajo CaDCC] Solicitud aceptada'

        send_email(self, subject, t, {})

    def get_closed_offers_without_feedback(self):
        from . import Offer
        return Offer.get_closed_without_feedback().filter(enterprise=self)

    def notify_rejection(self):
        t = get_template('mails/enterprise_rejection.html')
        subject = '[Bolsa Trabajo CaDCC] Solicitud rechazada'

        send_email(self, subject, t, {})

    @staticmethod
    def create_from_form(form):
        data = form.cleaned_data
        enterprise = Enterprise()
        enterprise.name = data['name']
        enterprise.rut = data['rut']
        enterprise.phone = data['phone']
        enterprise.address = data['address']
        enterprise.website = data['website']
        enterprise.description = data['description']
        enterprise.first_name = data['first_name']
        enterprise.last_name = data['last_name']
        enterprise.username = data['username']
        enterprise.email = data['email']
        enterprise.set_password(data['password'])
        #enterprise.is_active = False
        return enterprise

    def update_from_form(self, form):
        self.phone = form.cleaned_data['phone']
        self.address = form.cleaned_data['address']
        self.website = form.cleaned_data['website']
        self.description = form.cleaned_data['description']
        self.profile.block_public_access = form.cleaned_data['block_public_access']

    @staticmethod
    def get_pending_requests():
        #return Enterprise.objects.filter(is_active = False).filter(profile__validated_email = True)
        return Enterprise.objects.filter(profile__approved=False).filter(profile__validated_email=True)

    def save(self):
        same_username_users = User.objects.filter(username=self.username).filter(~Q(pk=self.id))
        if same_username_users:
            raise ValidationError('')
        super(Enterprise, self).save()

    def send_postulation_notification_email(self, postulation):
        subject = u'[Bolsa Trabajo CaDCC] Nueva postulación a oferta %s' % (unicode(postulation.offer),)

        t = get_template('mails/new_offer_postulation_mail.html')

        send_email(self, subject, t, {'postulation': postulation})

    class Meta:
        app_label = 'bolsa_trabajo'
