#-*- coding: UTF-8 -*-
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import Enterprise, OfferLevel, Tag
from BolsaTrabajo.bolsa_trabajo.utils import *

class Offer(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank = True, null = True)
    liquid_salary = models.IntegerField()
    level = models.ManyToManyField(OfferLevel)
    creation_date = models.DateTimeField(auto_now_add = True)
    available_slots = models.IntegerField()
    closed = models.BooleanField(default = False)
    has_unread_comments = models.BooleanField(default = False)
    validated = models.BooleanField(default = False)
    
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
        
    @staticmethod
    def get_pending_requests():
        return Offer.objects.filter(validated = False)
        
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
        offers = Offer.objects.filter(closed = False).filter(validated = True).order_by('-creation_date')
        if not include_hidden:
            offers = offers.filter(enterprise__profile__block_public_access = False)
        
        if form.is_valid():
            data = form.cleaned_data
            if data['enterprise']:
                offers = offers.filter(enterprise = data['enterprise'])
            if data['liquid_salary']:
                print data['liquid_salary']
                offers = offers.filter(Q(liquid_salary__gte = data['liquid_salary']) | Q(liquid_salary = 0))
            if not data['include_unavailable_salaries']:
                offers = offers.filter(liquid_salary__gt = 0)
            if data['level']:
                offers = offers.filter(level__in = data['level']).distinct()
            if data['tags']:
                tags = Tag.parse_string(data['tags'])
                if tags:
                    offers = offers.filter(tags__in = tags).distinct()
                    for offer in offers:
                        offer.affinity = offer.get_affinity(tags)
                    offers = sorted(offers, key = lambda offer: offer.affinity, reverse = True)
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
        from bolsa_trabajo.utils import send_email
        
        t = get_template('mails/offer_acceptance.html')
        subject = '[Bolsa Trabajo CaDCC] Oferta aceptada'

        send_email(self.enterprise, subject, t, {'offer': self})
        
    def notify_rejection(self):
        from bolsa_trabajo.utils import send_email
        
        t = get_template('mails/offer_rejection.html')
        subject = '[Bolsa Trabajo CaDCC] Oferta rechazada'

        send_email(self.enterprise, subject, t, {'offer': self})

    def __unicode__(self):
        return unicode(self.title)
    
    class Meta:
        app_label = 'bolsa_trabajo'
