from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from models.enterprise import Enterprise

class NewEnterpriseTestCase(TestCase):

    def test_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code,200)
    
    def register_test_user(self):
        user = User()
        user.username = 'test'
        user.set_password('test')
        user.is_staff = True
        user.save()
    
    def test_new_enterprise_view(self):
        register_test_user()
        self.client.login(username='test',password='test')
        resp = self.client.get('/account/new_enterprise')
        self.assertEqual(resp["Location"],'http://testserver/account/new_enterprise/')
        
    def test_new_enterprise_register(self):
        register_test_user()
        self.client.login(username='test',password='test')
        
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
