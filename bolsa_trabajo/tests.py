"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models.enterprise import Enterprise

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
