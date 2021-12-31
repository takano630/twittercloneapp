from django.test import TestCase
from .models import Account
from django.urls import reverse
from django.test import Client
client = Client()

class AccountTest(TestCase):
  def setUp(self):
    test = Account.objects.create(username='testpeople',email = 'test@test',password = 'testpasward',age='1')
    test.save()

  def test_status(self):
    response = client.get(reverse('signup'))
    self.assertEqual(response.status_code, 200)

  def test_number(self):
    number = Account.objects.count()
    self.assertEqual(number,1)
