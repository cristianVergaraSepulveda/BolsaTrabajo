# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from bolsa_trabajo.models.enterprise import Enterprise
from bolsa_trabajo.models.student import Student
from bolsa_trabajo.models.student_level import StudentLevel
from bolsa_trabajo.models.offer import Offer
from django.core.exceptions import ObjectDoesNotExist

class OfferStatusTestCase(TestCase):
    fixtures = ['users.json', 'enterprises.json', 'tags.json', 'offers.json']

    def aproveEnterprise(self):
        user = User.objects.get(username='test-enterprise3')
        user.profile.approved = True
        user.profile.validated_email = True
        user.profile.save()

    def assertNumberPendingOffers(self, num):
        resp = self.client.get('/account/pending_offer_request/5/')
        self.assertEqual(200,resp.status_code)

        # test messages
        self.assertTrue('Ver ofertas pasadas de esta empresa ('+num+' pendiente(s))' in resp.content)

    def assertPendingOffersMessages(self, message1, message2, message3):
        resp = self.client.get('/account/closed_offers/4/')
        self.assertEqual(200,resp.status_code)

        # test messages
        self.assertTrue("Enterprise3" in resp.content)
        self.assertTrue("<b>Teléfono:</b> 222" in resp.content)
        self.assertTrue("<b>Email:</b> test@example.com" in resp.content)
        self.assertTrue("Offer7" in resp.content)
        self.assertTrue(message1 in resp.content)
        self.assertTrue("Offer8" in resp.content)
        self.assertTrue(message2 in resp.content)

        self.assertTrue(message3 in resp.content)

    def test_view(self):
        # login as test staff user
        self.client.login(username='test',password='test')
        self.assertNumberPendingOffers('2')


    def test_closed_offers_view(self):
        # login as test staff user
        self.client.login(username='test',password='test')
        self.assertPendingOffersMessages('No se ha establecido una raz','No se ha establecido una raz','')

    def test_change_offers_view(self):
        # login as test staff user
        self.client.login(username='test',password='test')

        resp = self.client.get('/account/change_offer_status/7/')
        self.assertEqual(200,resp.status_code)

        # test messages
        self.assertTrue('Offer7' in resp.content)
        self.assertTrue('Enterprise3' in resp.content)

    def test_change_offers(self):
        # login as test staff user
        self.client.login(username='test',password='test')
        status_name = 'No se ha contratado a nadie'

        # create dictionary with status info
        new_offer_data = {'status':5}

        # do a POST request including the new status
        resp = self.client.post('/account/change_offer_status/7/',new_offer_data)

        # get the new Offer object from the database
        new_offer = Offer.objects.get(title='Offer7')

        # assert that the Offer object has the expected status
        self.assertEqual(new_offer.get_status_name(),status_name)

        # assert the message in closed offers site
        self.assertPendingOffersMessages(new_offer.get_status_name(),'No se ha establecido una raz','Feedback editado exitosamente')

        # test changes in pending offer site
        self.assertNumberPendingOffers('1')


