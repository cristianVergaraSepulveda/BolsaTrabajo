from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from bolsa_trabajo.models.enterprise import Enterprise
from bolsa_trabajo.models.student import Student
from bolsa_trabajo.models.student_level import StudentLevel

class NewEnterpriseTestCase(TestCase):

    fixtures = ['users.json','enterprises.json']

    def test_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code,200)

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

        # logout
        self.client.logout()

        # when logging in using the new enterprise username and password, the login function should return True
        self.assertTrue(self.client.login(username='test-enterprise',password='test-enterprise'))

    def test_data_enterprise_fixture(self):
        ent = Enterprise.objects.get(name='Enterprise1')
        self.assertEqual(ent.rut,'17.847.192-2')
