from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from bolsa_trabajo.models.enterprise import Enterprise
from bolsa_trabajo.models.student import Student
from bolsa_trabajo.models.student_level import StudentLevel
'''
class OfferTestCase(TestCase):

    fixtures = ['users.json', 'enterprises.json', 'tags.json', 'offers.json']

    def test_empty_search_form(self):
        # do a get request with no data for the search form
        resp = self.client.get('/offer/')
        self.assertEqual(200,resp.status_code)

        # the page should show all offers defined in offers.json
        self.assertTrue('Offer1' in resp.content)
        self.assertTrue('Offer2' in resp.content)
        self.assertTrue('Offer3' in resp.content)
        self.assertTrue('Offer4' in resp.content)

    def test_search_positive(self):
        get_data = {
            'enterprise':3,
            'liquid_salary': 75000,
            'include_unavailable_salaries':'off',
            'tags':'Tag1'}

        # do a get request using 'get_data' for the search form
        resp = self.client.get('/offer/',get_data)
        self.assertEqual(200,resp.status_code)

        # the message 'No se encontraron ofertas' shouldn't be shown
        self.assertFalse('No se encontraron ofertas' in resp.content)

        # Offer2 should be found and shown in the page
        self.assertTrue('Offer4' in resp.content)

    def test_search_negative(self):
        get_data = {
            'enterprise':3,
            'liquid_salary': 1000000,
            'include_unavailable_salaries':'off',
            'tags':'Tag1'}

        # do a get request using 'get_data' for the search form
        resp = self.client.get('/offer/',get_data)
        self.assertEqual(200,resp.status_code)

        # the message 'No se encontraron ofertas' should be shown
        self.assertTrue('No se encontraron ofertas' in resp.content)
'''