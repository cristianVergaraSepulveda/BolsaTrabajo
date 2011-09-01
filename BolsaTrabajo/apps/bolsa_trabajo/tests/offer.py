# coding: utf-8

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from ..models.offer import Offer


class OfferTestCase(TestCase):
    fixtures = ['users.json', 'enterprises.json', 'tags.json', 'offers.json', 'offers_expiration.json']

    def test_empty_search_form(self):
        # do a get request with no data for the search form
        resp = self.client.get('/offer/')
        self.assertEqual(200, resp.status_code)

        # the page should show all offers defined in offers.json
        self.assertTrue('Offer1' in resp.content)
        self.assertTrue('Offer2' in resp.content)
        self.assertTrue('Offer3' in resp.content)
        self.assertTrue('Offer4' in resp.content)

    def test_search_positive(self):
        get_data = {
            'enterprise': 3,
            'liquid_salary': 75000,
            'include_unavailable_salaries': 'off',
            'tags': 'Tag1'}

        # do a get request using 'get_data' for the search form
        resp = self.client.get('/offer/', get_data)
        self.assertEqual(200, resp.status_code)

        # the message 'No se encontraron ofertas' shouldn't be shown
        self.assertFalse('No se encontraron ofertas' in resp.content)

        # Offer2 should be found and shown in the page
        self.assertTrue('Offer4' in resp.content)

    def test_search_negative(self):
        get_data = {
            'enterprise': 3,
            'liquid_salary': 1000000,
            'include_unavailable_salaries': 'off',
            'tags': 'Tag1'}

        # do a get request using 'get_data' for the search form
        resp = self.client.get('/offer/', get_data)
        self.assertEqual(200, resp.status_code)

        # the message 'No se encontraron ofertas' should be shown
        self.assertTrue('No se encontraron ofertas' in resp.content)

    def test_accept_offer(self):
        # get the pending Offer object from the database
        pending_offer = Offer.objects.get(pk=5)
        self.assertEqual(pending_offer.status,1)

        # login as test staff user
        self.client.login(username='test', password='test')

        # do a get request without data for the accept page
        resp = self.client.post('/account/pending_offer_request/5/accept/')
        self.assertEqual(302, resp.status_code)

        # logout
        self.client.logout()

        # get the accepted Offer object from the database
        pending_offer = Offer.objects.get(pk=5)

        # assert that the Offer is now accepted
        self.assertEqual(pending_offer.status,2)

    def test_reject_offer(self):
        # get the pending Offer object from the database
        pending_offer = Offer.objects.get(pk=5)
        self.assertEqual(pending_offer.status,1)

        # login as test staff user
        self.client.login(username='test', password='test')

        # do a get request without data for the reject page
        resp = self.client.post('/account/pending_offer_request/5/reject/')
        self.assertEqual(302, resp.status_code)

        # logout
        self.client.logout()

        # assert that the rejected Offer is now deleted
        self.assertRaises(ObjectDoesNotExist, Offer.objects.get, pk="5")
