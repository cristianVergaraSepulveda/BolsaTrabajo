# coding: utf-8

from django.test import TestCase

from ..models.offer import Offer


class OfferStatisticsTestCase(TestCase):
    fixtures = ['users.json', 'enterprises.json', 'tags.json', 'offers_statistics_tests.json']
