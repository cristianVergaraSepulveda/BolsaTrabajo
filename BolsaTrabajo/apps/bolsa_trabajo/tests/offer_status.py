# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User

from ..models.offer import Offer


class OfferStatusTestCase(TestCase):
    fixtures = ['users.json', 'enterprises.json', 'tags.json', 'offers.json']

    def aproveEnterprise(self):
        user = User.objects.get(username='test-enterprise3')
        user.profile.approved = True
        user.profile.validated_email = True
        user.profile.save()

    def assertPendingOffersMessages(self, message1, message2, message3):
        resp = self.client.get('/account/closed_offers/4/')
        self.assertEqual(200, resp.status_code)

        # test messages
        self.assertTrue("Enterprise3" in resp.content)
        self.assertTrue("fono:</b> 222" in resp.content)
        self.assertTrue("Email:</b> test@example.com" in resp.content)
        self.assertTrue("Offer7" in resp.content)
        self.assertTrue(message1 in resp.content)
        self.assertTrue("Offer8" in resp.content)      
        self.assertTrue(message2 in resp.content)
        self.assertTrue(message3 in resp.content)

    def test_view(self):
        # login as test staff user
        self.client.login(username='test',password='test')
        # self.assertNumberPendingOffers('2')


    def test_closed_offers_view(self):
        # login as test staff user
        self.client.login(username='test',password='test')
        self.assertPendingOffersMessages('No se especific','No se especific','')

    def test_change_offers_view(self):
        # login as test staff user
        self.client.login(username='test', password='test')

        resp = self.client.get('/account/change_offer_status/7/')
        self.assertEqual(200, resp.status_code)

        # test messages
        self.assertTrue('Offer7' in resp.content)
        self.assertTrue('Enterprise3' in resp.content)

    def test_change_offers(self):
        # login as test staff user
        self.client.login(username='test',password='test')
        status_name = u'La oferta de trabajo ya no aplica'

        # create dictionary with status info
        new_offer_data = {'closure_reason':2}

        # do a POST request including the new status
        resp = self.client.post('/account/change_offer_status/7/', new_offer_data)

        # get the new Offer object from the database
        new_offer = Offer.objects.get(title='Offer7')

        # assert that the Offer object has the expected status
        self.assertEqual(new_offer.get_closure_reason_name(),status_name)

        # assert the message in closed offers site
        self.assertPendingOffersMessages(new_offer.get_closure_reason_name(), 'No se especific','Feedback editado exitosamente')

        # test changes in pending offer site
        # self.assertNumberPendingOffers('1')


    def test_view_all_closed_offers(self):
        # login as test staff user
        self.client.login(username='test', password='test')
        resp = self.client.get('/account/all_closed_offers/')
        self.assertEqual(200, resp.status_code)
        # assert that messages are correct
        self.assertTrue('Enterprise3</a> (2 pendiente(s))' in resp.content)

