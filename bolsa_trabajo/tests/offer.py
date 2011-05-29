from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from bolsa_trabajo.models.enterprise import Enterprise
from bolsa_trabajo.models.student import Student
from bolsa_trabajo.models.student_level import StudentLevel

class OfferTestCase(TestCase):

    fixtures = ['users.json', 'enterprises.json', 'tags.json', 'offers.json']

    def test_search_positive(self):
        get_data = {
            'enterprise':3,
            'liquid_salary': 75000,
            'include_unavailable_salaries':'on',
            'tags':'Tag1'}

        resp = self.client.get('/offer/',get_data)
        self.assertEqual(200,resp.status_code)
        self.assertFalse('No se encontraron ofertas' in resp.content)
