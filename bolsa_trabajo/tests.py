"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

#from django.test import TestCase

#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.failUnlessEqual(1 + 1, 2)

#__test__ = {"doctest": """
#Another way to test that 1 + 1 is equal to 2.

#>>> 1 + 1 == 2
#True
#"""}

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth

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
        #self.client.login

