# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from bolsa_trabajo.models.enterprise import Enterprise
from bolsa_trabajo.models.student import Student
from bolsa_trabajo.models.student_level import StudentLevel
from bolsa_trabajo.models.offer import Offer
from django.core.exceptions import ObjectDoesNotExist

class OfferStatisticsTestCase(TestCase):
    fixtures = ['users.json', 'enterprises.json', 'tags.json', 'offers_statistics_tests.json']
