from django.test import TestCase
from .models import Account
from django.urls import reverse
from django.test import Client
client = Client()

class AccountCreateTest(TestCase):
  def setUp(self):
   self.test_people = Account.objects.create(username='testpeople',email = 'test@test.test',password = 'testpassword',age='1')

  def test_status(self):
    response = client.get(reverse('signup'))
    self.assertEqual(response.status_code,200)

  def test_user_number(self):
    user_count = Account.objects.count()
    self.assertEqual(user_count,1)

  def test_people_data(self):
    self.assertEqual(self.test_people.username,'testpeople')
    self.assertEqual(self.test_people.email,'test@test.test')
    self.assertEqual(self.test_people.password,'testpassword')
    self.assertEqual(self.test_people.age,'1')
  
class SuccessfulSignUpTest(TestCase):
  def setUp(self):
    url = reverse('signup')
    data = {'username':'people','email':'test@test.test','password1':'testpassword','password2':'testpassword','age':'1'}
    self.response = self.client.post(url,data)
 
  def test_user_creation(self):
        self.assertTrue(Account.objects.exists())


class InvalidSignUpTest(TestCase):
  def setUp(self):
    url = reverse('signup')
    data = {}
    self.response = self.client.post(url,data)

  def test_signup_status(self):
    self.assertEquals(self.response.status_code,200)

  def test_dont_create_user(self):
        self.assertFalse(Account.objects.exists())


class SameNameSignUpTest(TestCase):
  def setUp(self):
    url = reverse('signup')
    data = {'username':'people','email':'test@test.test','password1':'testpassword','password2':'testpassword','age':'1'}
    self.response = self.client.post(url,data)
    same_name_data = {'username':'people','email':'testtest@test.test','password1':'testtestpassword','password2':'testtestpassword','age':'3'}
    self.response = self.client.post(url,same_name_data)

  def test_same_name_signup(self):
    user_count = Account.objects.count()
    self.assertEqual(user_count,1)

