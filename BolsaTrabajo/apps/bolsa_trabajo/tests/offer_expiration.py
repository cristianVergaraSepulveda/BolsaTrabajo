# coding: utf-8

from datetime import datetime
from datetime import timedelta

from ..models import Offer

from django.conf import settings
from django.test import TestCase


class OfferExpirationTestCase(TestCase):
    fixtures = ['users.json', 'enterprises.json', 'tags.json', 'test_offers_expiration.json']

    '''
    def test_offers_expiration(self):
        unexpired_open_offer = Offer.objects.get(pk=100)
        expired_open_offer = Offer.objects.get(pk=101)
        unexpired_closed_offer = Offer.objects.get(pk=102)
        expired_closed_offer = Offer.objects.get(pk=103)

        # prepare offer dates
        now = datetime.now()
        unexpired_open_offer.creation_date = now
        unexpired_closed_offer.creation_date = now
        expired_open_offer.creation_date = now - timedelta(days=(settings.OFFER_MAX_EXPIRATION_LIMIT + 1))
        expired_closed_offer.creation_date = now - timedelta(days=(settings.OFFER_MAX_EXPIRATION_LIMIT + 1))
        unexpired_open_offer.save()
        unexpired_closed_offer.save()
        expired_open_offer.save()
        expired_closed_offer.save()

        # should discard closed offers
        unexpired_offers = Offer.get_unexpired().order_by('id')
        expired_offers = Offer.get_expired().order_by('id')

        self.assertSequenceEqual([unexpired_open_offer], unexpired_offers.order_by('id'))
        self.assertSequenceEqual([expired_open_offer], expired_offers.order_by('id'))   
    '''
