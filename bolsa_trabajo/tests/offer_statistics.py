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

    @staticmethod
    def count_concreted_offers(enterprise_name):
        concreted_offers = Offer.objects.exclude(status=1).exclude(status=4).exclude(status=5)
        num_concreted_offers = 0
        for offer in concreted_offers:
            if offer.enterprise.name == enterprise_name:
                num_concreted_offers += 1
        return num_concreted_offers

    @staticmethod
    def count_non_concreted_offers(enterprise_name):
        non_concreted_offers = Offer.objects.exclude(status=2).exclude(status=3)
        num_non_concreted_offers = 0
        for offer in non_concreted_offers:
            if offer.enterprise.name == enterprise_name:
                num_non_concreted_offers += 1
        return num_non_concreted_offers

    def assert_concreted_offers(self,enterprise_name,num_concreted):
        concreted_count = OfferStatisticsTestCase.count_concreted_offers(enterprise_name)
        self.assertEqual(concreted_count,num_concreted)

    def assert_non_concreted_offers(self,enterprise_name,num_non_concreted):
        non_concreted_count = OfferStatisticsTestCase.count_non_concreted_offers(enterprise_name)
        self.assertEqual(non_concreted_count,num_non_concreted)

    def test_statistics_view(self):
        # login as test staff user
        self.client.login(username='test',password='test')
        # go to statistics
        resp = self.client.get('/account/statistics/')
        self.assertEqual(200,resp.status_code)

        # Offer1 and Offer2 belong to Enterprise1, should be counted as concreted
        self.assert_concreted_offers('Enterprise1',2)
        self.assert_non_concreted_offers('Enterprise1',0)

        # Offer3 and Offer4 belong to Enterprise2, should be counted as non-concreted
        self.assert_concreted_offers('Enterprise2',0)
        self.assert_non_concreted_offers('Enterprise2',2)

    def test_offer_concreted_status_updated_by_enterprise(self):
        # login as Enterprise2
        self.client.login(username='test-enterprise2',password='test')
        # close Offer3
        resp = self.client.get('/account/offer/3/close/')
        # logout
        self.client.logout()

        # login as test staff user
        self.client.login(username='test',password='test')
        # go to control panel
        resp = self.client.get('/account/')
        # notification for closed offer should be shown
        self.assertTrue('Ofertas laborales pasadas (1)' in resp.content)
        # logout
        self.client.logout()

        # login as Enterprise2
        self.client.login(username='test-enterprise2',password='test')
        # set 'Se contrató a más de un postulante utilizando este medio' as the reason Offer3 was closed
        new_offer_status = {'status':2}
        resp = self.client.post('/account/offer/3/',new_offer_status)
        # logout
        self.client.logout()

        # login as test staff user
        self.client.login(username='test',password='test')
        # go to offer statistics
        resp = self.client.get('/account/statistics/')

        # assert that offers are counted correctly
        # Offer3 should be concreted
        self.assert_concreted_offers('Enterprise2',1)
        self.assert_non_concreted_offers('Enterprise2',1)
        offer3 = Offer.objects.get(pk=3)
        self.assertEqual(offer3.status,2)

    def test_offer_concreted_status_updated_by_staff(self):
        # login as Enterprise2
        self.client.login(username='test-enterprise2',password='test')
        # close Offer3
        resp = self.client.get('/account/offer/3/close/')
        # logout
        self.client.logout()

        # login as test staff user
        self.client.login(username='test',password='test')
        # go to control panel
        resp = self.client.get('/account/')
        # notification for closed offer should be shown
        self.assertTrue('Ofertas laborales pasadas (1)' in resp.content)
        # set 'Se contrató sólo a un estudiante utilizando este medio' as the reason Offer3 was closed
        new_offer_status = {'status':3}
        resp = self.client.post('/account/change_offer_status/3/',new_offer_status)
        # go to offer statistics
        resp = self.client.get('/account/statistics/')
        # logout
        self.client.logout()

        # assert that offers are counted correctly
        # Offer3 should be concreted
        self.assert_concreted_offers('Enterprise2',1)
        self.assert_non_concreted_offers('Enterprise2',1)
        offer3 = Offer.objects.get(pk=3)
        self.assertEqual(offer3.status,3)

    def test_offer_non_concreted_status_updated_by_enterprise(self):
        # login as Enterprise1
        self.client.login(username='test-enterprise1',password='test')
        # set 'Se contrató sólo postulantes fuera de este medio' as the reason Offer1 was closed
        new_offer_status = {'status':4}
        resp = self.client.post('/account/offer/1/',new_offer_status)
        # logout
        self.client.logout()

        # login as test staff user
        self.client.login(username='test',password='test')
        # go to offer statistics
        resp = self.client.get('/account/statistics/')

        # assert that offers are counted correctly
        # Offer1 should be non-concreted
        self.assert_concreted_offers('Enterprise1',1)
        self.assert_non_concreted_offers('Enterprise1',1)
        offer1 = Offer.objects.get(pk=1)
        self.assertEqual(offer1.status,4)

    def test_offer_non_concreted_status_updated_by_staff(self):
        # login as Enterprise1
        self.client.login(username='test-enterprise1',password='test')
        # set 'Se contrató sólo postulantes fuera de este medio' as the reason Offer1 was closed
        new_offer_status = {'status':4}
        resp = self.client.post('/account/offer/1/',new_offer_status)
        # logout
        self.client.logout()

        # login as test staff user
        self.client.login(username='test',password='test')
        # set 'Se contrató sólo postulantes fuera de este medio' as the reason Offer1 was closed
        new_offer_status = {'status':4}
        resp = self.client.post('/account/change_offer_status/1/',new_offer_status)
        # go to offer statistics
        resp = self.client.get('/account/statistics/')

        # assert that offers are counted correctly
        # Offer1 should be non-concreted
        self.assert_concreted_offers('Enterprise1',1)
        self.assert_non_concreted_offers('Enterprise1',1)
        offer1 = Offer.objects.get(pk=1)
        self.assertEqual(offer1.status,4)
