#-*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from bolsa_trabajo.models import Enterprise, OfferLevel, Tag

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
    
    @staticmethod
    def create_from_form(enterprise, form):
        data = form.cleaned_data
        offer = Offer()
        offer.enterprise = enterprise
        offer.title = data['title']
        offer.description = data['description']
        offer.liquid_salary = data['liquid_salary']
        offer.available_slots = data['available_slots']
        offer.save()
        tags = Tag.parse_string(data['tags'])
        for tag in tags:
            offer.tags.add(tag)
        offer.level = data['level']
        return offer

    def __unicode__(self):
        return unicode(self.title)
    
    class Meta:
        app_label = 'bolsa_trabajo'
