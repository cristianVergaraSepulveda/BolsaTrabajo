# coding: utf-8

from .models import *
from django.contrib import admin

admin.site.register(Enterprise)
admin.site.register(EnterpriseComment)
admin.site.register(Offer)
admin.site.register(OfferComment)
admin.site.register(OfferLevel)
admin.site.register(OfferMessage)
admin.site.register(OfferMessageRing)
admin.site.register(Student)
admin.site.register(StudentLevel)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Postulation)
admin.site.register(WorkRegistry)