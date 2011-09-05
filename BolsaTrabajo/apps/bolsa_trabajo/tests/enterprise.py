# coding: utf-8

import hashlib

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from ..models.enterprise import Enterprise
from ..models.offer import Offer
from ..models.utils import now_plus_min_end_date


class AdminNewEnterpriseTestCase(TestCase):
    """
    Test to register a new enterprise from the admin's view
    """

    fixtures = ['users.json', 'enterprises.json']

    def test_new_enterprise_view(self):
        self.client.login(username='test', password='test')
        resp = self.client.get('/account/new_enterprise/')
        self.assertEqual(200, resp.status_code)

    def test_new_enterprise_register(self):
        # login as test staff user
        self.client.login(username='test', password='test')

        # create dictionary with new enterprise info
        new_enterprise_data = {'name': 'Test Enterprise', 'rut': '12345678-9', 'phone': '1234567',
                               'address': 'Fake Street 123', 'website': 'http://www.example.com',
                               'description': 'Test Enterprise description', 'first_name': 'Test',
                               'last_name': 'Enterprise', 'email': 'test@example.com', 'username': 'test-enterprise',
                               'password': 'test-enterprise', 'repeat_password': 'test-enterprise'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/new_enterprise/', new_enterprise_data)

        # get the new Enterprise object from the database
        new_enterprise = Enterprise.objects.get(name='Test Enterprise')

        # assert that the Enterprise object has the expected username
        self.assertEqual(new_enterprise.username, 'test-enterprise')

        # assert that the Enterprise object is approved
        self.assertEqual(new_enterprise.profile.approved, True)

        # logout
        self.client.logout()

        # when logging in using the new enterprise username and password, the login function should return True
        self.assertTrue(self.client.login(username='test-enterprise', password='test-enterprise'))

    def test_data_enterprise_fixture(self):
        ent = Enterprise.objects.get(name='Enterprise1')
        self.assertEqual(ent.rut, '17.847.192-2')

# enterprise registration from a new user's view
class PublishEnterpriseTestCase(TestCase):
    fixtures = ['users.json', 'enterprises.json', 'offers.json', 'offers_level.json']

    def assert_and_check_messages(self, user, email_assertion, approval_assertion, param_username, param_password):
        self.client.login(username=param_username, password=param_password)
        resp = self.client.get('/account/')
        self.assertEqual(user.profile.validated_email, email_assertion)
        self.assertEqual(user.profile.approved, approval_assertion)
        if not email_assertion:
            self.assertTrue('Su correo electrónico aún no ha sido verificado' in resp.content)
        else:
            self.assertTrue('Cuenta de correo activada correctamente' in resp.content)
            if not approval_assertion:
                self.assertTrue(
                    'Su cuenta aún no ha sido validada personalmente por un encargado, por favor espere hasta ser contactado.' in resp.content)
        self.client.logout()

    def test_new_enterprise_view(self):
        resp = self.client.get('/account/register/enterprise/')
        self.assertEqual(200, resp.status_code)

    def test_new_enterprise_register(self):
        # create dictionary with new enterprise info
        new_enterprise_data = {'name': 'Test Enterprise', 'rut': '12345678-9', 'phone': '1234567',
                               'address': 'Fake Street 123', 'website': 'http://www.example.com',
                               'description': 'Test Enterprise description', 'first_name': 'Test',
                               'last_name': 'Enterprise', 'email': 'test@example.com', 'username': 'test-enterprise',
                               'password': 'test-enterprise', 'repeat_password': 'test-enterprise'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/register/enterprise/', new_enterprise_data)

        # get the new enterprise object from the database
        new_enterprise = Enterprise.objects.get(name='Test Enterprise')

        # assert that the enterprise object has the expected username
        self.assertEqual(new_enterprise.username, 'test-enterprise')

        # the email account shouldn't be validated yet
        self.assert_and_check_messages(new_enterprise, email_assertion=False, approval_assertion=False,
                                       param_username='test-enterprise', param_password='test-enterprise')

        '''
        # the email account shouldn't be validated yet
        self.assertFalse(new_enterprise.profile.validated_email)

        # message about email validation should be shown to the user
        self.client.login(username='test-enterprise',password='test-enterprise')
        resp = self.client.get('/account/')
        self.assertTrue('Su correo electrónico aún no ha sido verificado' in resp.content)
        '''

    def validate_enterprise3_email_and_check(self):
        # utility method, validates the email account of test-enterprise3 defined in enterprises.json

        # login as Enterprise3
        self.client.login(username='test-enterprise3', password='test')

        # generate key that Enterprise3 got in their email
        user = User.objects.get(username='test-enterprise3')
        key = hashlib.sha224(settings.SECRET_KEY + user.username + user.email).hexdigest()

        # go to validation URL
        resp = self.client.get('/account/validate_email/', {'validation_key': key})

        # assert that the email account was validated
        enterprise3 = Enterprise.objects.get(username='test-enterprise3')
        self.assert_and_check_messages(enterprise3, email_assertion=True, approval_assertion=False,
                                       param_username='test-enterprise3', param_password='test')

        '''
        # the email account should be validated
        self.assertTrue(new_enterprise.profile.validated_email)

        # message about email validation should be shown to the user
        self.client.login(username='test-enterprise',password='test-enterprise')
        resp = self.client.get('/account/')
        self.assertTrue('Cuenta de correo activada correctamente' in resp.content)
        '''

    def test_pending_enterprise_view(self):
        # validate email
        self.validate_enterprise3_email_and_check()

        # enterprise3 shouldn't be approved yet
        enterprise = Enterprise.objects.get(username='test-enterprise3')
        self.assertFalse(enterprise.profile.approved)

        # login as test staff user
        self.client.login(username='test', password='test')

        # go to pending enterprise requests
        resp = self.client.get('/account/pending_enterprise_request/')

        # Enterprise3 should be displayed
        self.assertTrue('Enterprise3' in resp.content)

    def test_accept_pending_request(self):
        # validate email
        self.validate_enterprise3_email_and_check()

        # login as test staff user
        self.client.login(username='test', password='test')

        # accept Enterprise3's request
        resp = self.client.get('/account/pending_enterprise_request/4/accept/')

        # logout
        self.client.logout()

        # enterprise3 should be approved
        enterprise3 = Enterprise.objects.get(name='Enterprise3')
        self.assertTrue(enterprise3.profile.approved)

    def test_reject_pending_request(self):
        # validate email
        self.validate_enterprise3_email_and_check()

        # login as test staff user
        self.client.login(username='test', password='test')

        # reject Enterprise3's request
        resp = self.client.get('/account/pending_enterprise_request/4/reject/')

        self.client.logout()

        # Enterprise3 should not be able to login
        self.assertFalse(self.client.login(username='test-enterprise3', password='test'))

        # Enterprise3 should be deleted from the database
        self.assertRaises(ObjectDoesNotExist, Enterprise.objects.get, name='Enterprise3')


    #Offers Tests

    # def test_new_offer_view(self):
    #     self.test_accept_pending_request()
    #     self.assertTrue(self.client.login(username='test-enterprise3', password='test'))
    #     resp = self.client.get('/account/offer/add')
    #     self.assertEqual(200, resp.status_code)

    #     self.assertTrue(
    #         'Haga click <a href="http://www.dcc.uchile.cl/node/230" target="_blank">aqu&iacute;</a> e ingrese a la secci&oacute;n "Recomendaciones para pr&aacute;cticas profesionales" para obtener informaci&oacute;n sobre los distintos requerimientos de cada nivel de pr&aacute;tica.' in resp.content)

    def test_new_offer_regiter(self):
        self.test_accept_pending_request()
        self.assertTrue(self.client.login(username='test-enterprise3', password='test'))

        # create dictionary with new offer info
        new_offer_data = {'title': 'Oferta1', 'description': 'oferta num 1', 'liquid_salary': 0,
                          'available_slots': '2', 'level': 1, 'tags': 'SQL'}

        # do a POST request including the new offer
        resp = self.client.post('/account/offer/add', new_offer_data)

        self.assertEqual(302, resp.status_code)
        self.assertEqual('http://testserver'+reverse('bolsa_trabajo.views_enterprise.offer'), resp['Location'])

        # # get the new Offer object from the database
        # new_offer = Offer.objects.get(title='Oferta1')

        # # assert that the Offer object has the expected description
        # self.assertEqual(new_offer.description, 'oferta num 1')

        # # assert that the Offer object is not validated
        # self.assertTrue(new_offer.is_pending())

        # # assert the message
        # resp = self.client.get('/account/')
        # self.assertTrue('Oferta propuesta exitosamente, por favor espere a que un encargado la valide' in resp.content)


    # def test_offer_view(self):
    #     self.test_accept_pending_request()
    #     self.assertTrue(self.client.login(username='test-enterprise3', password='test'))

    #     # verufy the status of the site
    #     resp = self.client.get('/account/offer/')
    #     self.assertEqual(200, resp.status_code)

    #     # the page should show all offers defined in offers.json in their determinated sections
    #     #Pending
    #     self.assertTrue('<a href="/account/offer/5/edit">Offer5</a>' in resp.content)
    #     #Active
    #     self.assertTrue('<a href="/offer/6/">Offer6</a> (<a href="/account/offer/6/edit">Editar</a>)' in resp.content)
    #     #Closed
    #     self.assertTrue('<a href="/account/offer/7/">Offer7</a>' in resp.content)
    #     self.assertTrue('No se especific' in resp.content)


    def test_offer_edit_view(self):
        self.test_accept_pending_request()
        self.assertTrue(self.client.login(username='test-enterprise3', password='test'))

        # verufy the status of the site
        resp = self.client.get('/account/offer/6/edit')
        self.assertEqual(200, resp.status_code)

        # the page should show the offer's edit form
        self.assertTrue('Offer6' in resp.content)
        self.assertTrue('1500000' in resp.content)
        self.assertFalse('$ 1500000' in resp.content)

        # create dictionary to edit the offer
        end_date = now_plus_min_end_date().isoformat()
        new_offer_data = {'title': 'Oferta1', 'description': 'oferta num 1', 'liquid_salary': 0,
                          'available_slots': '2', 'level': 1, 'end_date': end_date, 'tags': 'SQL'}

        # do a POST request including the new offer info
        resp = self.client.post('/account/offer/6/edit', new_offer_data)

        # get the edited Offer object from the database
        new_offer = Offer.objects.get(title='Oferta1')

        # assert that the Offer object has the expected description
        self.assertEqual(new_offer.liquid_salary, 0)

        resp = self.client.get('/account/offer/6/')
        self.assertTrue('Oferta editada exitosamente' in resp.content)

    def test_offer_details_view(self):
        self.test_accept_pending_request()
        self.assertTrue(self.client.login(username='test-enterprise3', password='test'))

        # verufy the status of the site
        resp = self.client.get('/account/offer/7/')
        self.assertEqual(200, resp.status_code)
        # the page should show the offer's details
        self.assertTrue('Offer7' in resp.content)
        self.assertTrue('$ 1.500.000' in resp.content)

        # create dictionary with status info
        status_name = 'La oferta de trabajo ya no aplica'
        new_offer_data = {'closure_reason':2}

        # do a POST request including the new status
        resp = self.client.post('/account/offer/7/', new_offer_data)

        # get the new Offer object from the database
        new_offer = Offer.objects.get(title='Offer7')

        # assert that the Offer object has the expected status
        self.assertEqual(new_offer.get_closure_reason_name(),status_name)

        # assert the message in the site
        resp = self.client.get('/account/offer/')
        self.assertTrue('Feedback editado exitosamente' in resp.content)

