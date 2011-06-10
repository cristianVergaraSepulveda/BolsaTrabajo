import settings
import hashlib
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from bolsa_trabajo.models.enterprise import Enterprise
from bolsa_trabajo.models.student import Student
from bolsa_trabajo.models.user_profile import UserProfile
from bolsa_trabajo.models.student_level import StudentLevel

#Test to register a new enterprise from the admin's view
class AdminNewEnterpriseTestCase(TestCase):

    fixtures = ['users.json','enterprises.json']

    def test_new_enterprise_view(self):
        self.client.login(username='test',password='test')
        resp = self.client.get('/account/new_enterprise/')
        self.assertEqual(200,resp.status_code)

    def test_new_enterprise_register(self):
        # login as test staff user
        self.client.login(username='test',password='test')

        # create dictionary with new enterprise info
        new_enterprise_data = {'name':'Test Enterprise', 'rut':'12345678-9', 'phone':'1234567', 'address':'Fake Street 123', 'website':'http://www.example.com', 'description':'Test Enterprise description', 'first_name':'Test', 'last_name':'Enterprise', 'email':'test@example.com', 'username':'test-enterprise', 'password':'test-enterprise', 'repeat_password':'test-enterprise'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/new_enterprise/',new_enterprise_data)

        # get the new Enterprise object from the database
        new_enterprise = Enterprise.objects.get(name='Test Enterprise')

        # assert that the Enterprise object has the expected username
        self.assertEqual(new_enterprise.username,'test-enterprise')

        # assert that the Enterprise object is approved
        self.assertEqual(new_enterprise.profile.approved,True)

        # logout
        self.client.logout()

        # when logging in using the new enterprise username and password, the login function should return True
        self.assertTrue(self.client.login(username='test-enterprise',password='test-enterprise'))

    def test_data_enterprise_fixture(self):
        ent = Enterprise.objects.get(name='Enterprise1')
        self.assertEqual(ent.rut,'17.847.192-2')


#Test to register a new enterprise from a new user's view
class NewEnterpriseTestCase(TestCase):

    fixtures = ['users.json','enterprises.json']

    def test_new_enterprise_view(self):
        resp = self.client.get('/account/register/enterprise/')
        self.assertEqual(200,resp.status_code)

    def test_new_enterprise_register(self):

        # create dictionary with new enterprise info
        new_enterprise_data = {'name':'Test Enterprise', 'rut':'12345678-9', 'phone':'1234567', 'address':'Fake Street 123', 'website':'http://www.example.com', 'description':'Test Enterprise description', 'first_name':'Test', 'last_name':'Enterprise', 'email':'test@example.com', 'username':'test-enterprise', 'password':'test-enterprise', 'repeat_password':'test-enterprise'}

        # do a POST request including the new enterprise to be registered
        resp = self.client.post('/account/register/enterprise/',new_enterprise_data)

        # get the new enterprise object from the database
        new_enterprise = Enterprise.objects.get(name='Test Enterprise')

        # assert that the enterprise object has the expected username
        self.assertEqual(new_enterprise.username,'test-enterprise')

        # when logging in using the new enterprise username and password, the login function should return True
        self.assertTrue(self.client.login(username='test-enterprise',password='test-enterprise'))


class PublishEnterpriseTestCase(TestCase):

    fixtures = ['users.json','enterprises.json']

    def test_pending_enterprise_view(self):
        # validate email
        # login as Enterprise3
        self.client.login(username='test-enterprise3',password='test')

        # generate key that Enterprise3 got in their email
        user = User.objects.get(username='test-enterprise3')
        key = hashlib.sha224(settings.SECRET_KEY + user.username + user.email).hexdigest()

        # go to validation URL
        resp = self.client.get('/account/validate_email/',{'validation_key' : key})

        # assert that the email account was validated
        enterprise = Enterprise.objects.get(username='test-enterprise3')
        self.assertTrue(enterprise.profile.validated_email and not enterprise.profile.approved)

        # logout
        self.client.logout()

        # login as test staff user
        self.client.login(username='test',password='test')

        # go to pending enterprise requests
        resp = self.client.get('/account/pending_enterprise_request/')

        # Enterprise3 should be displayed
        self.assertTrue('Enterprise3' in resp.content)

    def test_accept_pending_request(self):
        # login as test staff user
        self.client.login(username='test',password='test')

        # accept Enterprise3's request
        resp = self.client.get('/account/pending_enterprise_request/4/accept/')

        self.client.logout()

        # Enterprise3 should be approved
        enterprise3 = Enterprise.objects.get(name='Enterprise3')
        self.assertTrue(enterprise3.profile.approved)

    def test_reject_pending_request(self):
        # login as test staff user
        self.client.login(username='test',password='test')

        # reject Enterprise3's request
        resp = self.client.get('/account/pending_enterprise_request/4/reject/')

        self.client.logout()

        # Enterprise3 should not be able to login
        self.assertFalse(self.client.login(username='test-enterprise3',password='test'))

        # Enterprise3 should be deleted from the database
        self.assertRaises(ObjectDoesNotExist,Enterprise.objects.get,name='Enterprise3')
