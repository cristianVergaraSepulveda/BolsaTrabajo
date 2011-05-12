from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from models.enterprise import Enterprise

class NewEnterpriseTestCase(TestCase):

    fixtures = ['new_enterprise_testdata.json']

    def test_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code,200)

    def test_new_enterprise_view(self):
        self.client.login(username='test',password='test')
        resp = self.client.get('/account/new_enterprise/')
        self.assertEqual(200,resp.status_code)
        #self.assertEqual(resp["Location"],'http://testserver/account/new_enterprise/')

    def test_new_enterprise_register(self):
        self.client.login(username='test',password='test')
        new_enterprise_data = {'name':'Test Enterprise', 'rut':'12345678-9', 'phone':'1234567', 'address':'Fake Street 123', 'website':'http://www.example.com', 'description':'Test Enterprise description', 'first_name':'Test', 'last_name':'Enterprise', 'email':'test@example.com', 'username':'test-enterprise', 'password':'test-enterprise', 'repeat_password':'test-enterprise'}
        resp = self.client.post('/account/new_enterprise/',new_enterprise_data)
        new_enterprise = Enterprise.objects.get(name='Test Enterprise')
        self.assertEqual(new_enterprise.name,'Test Enterprise')
        self.assertEqual(new_enterprise.rut,'12345678-9')
        self.assertEqual(new_enterprise.phone,'1234567')
        
class OffersViewsTestCase(TestCase):
    fixtures = ['offer_views_testdata.json']

    def test_offer(self):
        enterprise = Enterprise(name="foobar")
        enterprise.save()
        enterprises = Enterprise.objects.all()
        print(type(enterprises))
        for e in enterprises:
            print("record...")
            print(e.name)

        Enterprise.objects.get(name='pepito')
        resp = self.client.get('/offer/')
        self.assertEqual(resp.status_code, 200)
