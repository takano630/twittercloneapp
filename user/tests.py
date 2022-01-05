from django.test import TestCase
from .models import Account
from .forms import AccountCreateForm
from django.urls import reverse
from django.test import Client
client = Client()

class AccountCreateTest(TestCase):
  def setUp(self):
   global testpeople
   testpeople = Account.objects.create(username='testpeople',email = 'test@test.test',password = 'testpassword',age='1')

  def test_status(self):
    response = client.get(reverse('signup'))
    self.assertEqual(response.status_code, 200)

  def test_user_number(self):
    user_count = Account.objects.count()
    self.assertEqual(user_count,1)

  def test_people_data(self):
    self.assertEqual(testpeople.username,'testpeople')
    self.assertEqual(testpeople.email,'test@test.test')
    self.assertEqual(testpeople.password,'testpassword')
    self.assertEqual(testpeople.age,'1')
  
  def test_form(self):
    form = AccountCreateForm(data={'username':'people','email':'test@test.test','password1':'testpassword','password2':'testpassword','age':'1'})
    self.assertTrue(form.is_valid())

  def test_form_failed(self):
    form = AccountCreateForm(data={})
    self.assertFalse(form.is_valid())

  def test_same_name_user(self):
    Account.objects.create(username='sameperson',email = 'test@test.test',password = 'testpassword',age='1')
    form = AccountCreateForm(data={'username':'sameperson','email':'test@test.test','password1':'testpassword','password2':'testpassword','age':'1'})
    self.assertFalse(form.is_valid())