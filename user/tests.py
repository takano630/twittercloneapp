from django.test import TestCase
from .models import Account
from django.urls import reverse


class AccountCreateTest(TestCase):
  def setUp(self):
   self.test_people = Account.objects.create(username='testpeople',email = 'test@test.test',password = 'testpassword',age='1')

  def test_status(self):
    response = self.client.get(reverse('signup'))
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
    self.url = reverse('signup')
    data = {'username':'people','email':'test@test.test','password1':'testpassword','password2':'testpassword','age':'1'}
    self.response = self.client.post(self.url,data)

  def test_user_creation(self):
    self.assertTrue(Account.objects.exists())
    self.assertEquals(self.response.status_code,200)


class InvalidSignUpTest(TestCase):
  def setUp(self):
    self.url = reverse('signup')

  def test_post_empty(self):
    data = {}
    self.response = self.client.post(self.url,data)
    self.assertEquals(self.response.status_code,200)
    self.assertFalse(Account.objects.exists())

  def test_post_short_password(self):
    data = {'username':'people','email':'test@test.test','password1':'test','password2':'test','age':'1'}
    self.response = self.client.post(self.url,data)
    self.assertEquals(self.response.status_code,200)
    self.assertFalse(Account.objects.exists())

  def test_post_mistake_email(self):
    data = {'username':'people','email':'testtest.test','password1':'testpassword','password2':'testpassword','age':'1'}
    self.response = self.client.post(self.url,data)
    self.assertEquals(self.response.status_code,200)
    self.assertFalse(Account.objects.exists())

  def test_post_different_password1_password2(self):
      data = {'username':'people','email':'test@test.test','password1':'testpassword','password2':'testdifferent','age':'1'}
      self.response = self.client.post(self.url,data)
      self.assertEquals(self.response.status_code,200)
      self.assertFalse(Account.objects.exists())
    
  def test_post_only_number_password(self):
    data = {'username':'people','email':'test@test.test','password1':'20220108','password2':'20220108','age':'1'}
    self.response = self.client.post(self.url,data)
    self.assertEquals(self.response.status_code,200)
    self.assertFalse(Account.objects.exists())
  
  def test_post_similar_name_password(self):
    data = {'username':'testpeople','email':'test@test.test','password1':'testpeople','password2':'testpeople','age':'1'}
    self.response = self.client.post(self.url,data)
    self.assertEquals(self.response.status_code,200)
    self.assertFalse(Account.objects.exists())

  def test_post_general_password(self):
    data = {'username':'people','email':'test@test.test','password1':'password','password2':'password','age':'1'}
    self.response = self.client.post(self.url,data)
    self.assertEquals(self.response.status_code,200)
    self.assertFalse(Account.objects.exists())

  def test_post_duplicate_username(self):
    data = {'username':'people','email':'test@test.test','password1':'testpassword','password2':'testpassword','age':'1'}
    self.response = self.client.post(self.url,data)
    same_name_data = {'username':'people','email':'testtest@test.test','password1':'testtestpassword','password2':'testtestpassword','age':'3'}
    self.response = self.client.post(self.url,same_name_data)
    user_count = Account.objects.count()
    self.assertEqual(user_count,1)

