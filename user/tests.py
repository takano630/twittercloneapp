from django.test import TestCase
from django.urls import reverse, reverse_lazy

from .models import Account


class TopViewTests(TestCase):
  def setUp(self):
    self.response = self.client.get(reverse('top'))

  def test_top_status(self):
    self.assertEqual(self.response.status_code, 200)

  def test_top_html(self):
    self.assertTemplateUsed(self.response, 'top.html')


class AccountModelTests(TestCase):
  def setUp(self):
   self.data = {'username':'testpeople', 'email':'test@test.test', 'password':'testpassword', 'age':'1'}
   self.test_people = Account.objects.create(username=self.data['username'],email=self.data['email'],password=self.data['password'],age=self.data['age'])

  def test_user_number(self):
    user_count = Account.objects.count()
    self.assertEqual(user_count, 1)

  def test_people_data(self):
    self.assertEqual(self.test_people.username, self.data['username'])
    self.assertEqual(self.test_people.email, self.data['email'])
    self.assertEqual(self.test_people.password, self.data['password'])
    self.assertEqual(self.test_people.age, self.data['age'])


class SignUpTests(TestCase):
  def setUp(self):
    self.response = self.client.get(reverse('signup'))

  def test_status(self):
    self.assertEqual(self.response.status_code, 200)

  def test_html_signup(self):
    self.assertTemplateUsed(self.response, 'user/signup.html')
  

class SignUpSuccessTests(TestCase):
  def setUp(self):
    self.url = reverse('signup')
    data = {'username':'people', 'email':'test@test.test', 'password1':'testpassword', 'password2':'testpassword', 'age':'1'}
    self.response = self.client.post(self.url, data)

  def test_user_creation(self):
    self.assertTrue(Account.objects.exists())
    self.assertEquals(self.response.status_code, 200)

  def test_html_signup_success(self):
    self.assertTemplateUsed(self.response, 'user/signup_successed.html')


class SignUpFailTest(TestCase):
  def setUp(self):
    self.url = reverse('signup')
    self.data = {'username':'testpeople','email':'test@test.test','password1':'testpassword',
                 'password2':'testpassword','age':'1'}

  def test_post_empty(self):
    data = {}
    self.response = self.client.post(self.url, data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')

  def test_post_short_password(self):
    self.data['password1'] = 'test'
    self.data['password2'] = 'test'
    self.response = self.client.post(self.url, self.data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')

  def test_post_different_password1_password2(self):
      self.data['password1'] = 'testpassword',
      self.data['password2'] = 'testdifferent',
      self.response = self.client.post(self.url, self.data)
      self.assertEquals(self.response.status_code, 200)
      self.assertFalse(Account.objects.exists())
      self.assertTemplateUsed(self.response, 'user/signup.html')
    
  def test_post_only_number_password(self):
    self.data['password1'] = '20220108'
    self.data['password2'] = '20220108'
    self.response = self.client.post(self.url, self.data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')
  
  def test_post_similar_name_password(self):
    self.data['password1'] = 'testpeople'
    self.data['password2'] = 'testpeople'
    self.response = self.client.post(self.url, self.data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')

  def test_post_general_password(self):
    self.data['password1'] = 'password'
    self.data['password2'] = 'password'
    self.response = self.client.post(self.url, self.data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')

  def test_post_duplicate_username(self):
    self.response = self.client.post(self.url, self.data)
    same_name_data = {'username':'testpeople','email':'testtest@test.test','password1':'testtestpassword','password2':'testtestpassword','age':'3'}
    self.response = self.client.post(self.url, same_name_data)
    user_count = Account.objects.count()
    self.assertEqual(user_count, 1)
    self.assertTemplateUsed(self.response, 'user/signup.html')

  def test_post_mistake_email(self):
    self.data['email'] = 'testtest.test'
    self.response = self.client.post(self.url, self.data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')

  def test_post_blank_username(self):
    self.data['username'] = ''
    self.response = self.client.post(self.url, self.data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')

  def test_post_blank_email(self):
    self.data['email'] = ''
    self.response = self.client.post(self.url, self.data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')

  def test_post_blank_password(self):
    self.data['password1'] = ''
    self.data['password2'] = ''
    self.response = self.client.post(self.url, self.data)
    self.assertEquals(self.response.status_code, 200)
    self.assertFalse(Account.objects.exists())
    self.assertTemplateUsed(self.response, 'user/signup.html')


class LoginSuccessTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    self.home_url = reverse('home')
    self.login_url = reverse('login')

  def test_login_success(self):
    self.login_data = {'username':'people', 'password':'testpassword'}
    self.login_response = self.client.post(self.login_url, self.login_data)
    self.assertRedirects(self.login_response, self.home_url)


class LoginFailTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    self.home_url = reverse('home')
    self.login_url = reverse('login')
  
  def test_mistake_password(self):
    self.login_data = {'username':'people', 'password':'mistakepassword'}
    self.login_response = self.client.post(self.login_url, self.login_data)
    self.assertEqual(self.login_response.status_code, 200)

  def test_not_exist_user(self):
    self.login_data = {'username':'no_people', 'password':'testpassword'}
    self.login_response = self.client.post(self.login_url, self.login_data)
    self.assertEqual(self.login_response.status_code, 200)


class LogoutTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    self.top_url = reverse('top')
    self.login_url = reverse('login')
    self.login_data = {'username':'people', 'password':'testpassword'}
    self.client.post(self.login_url, self.login_data)

  def test_logout(self):
    self.logout_url = reverse('logout')
    self.logout_response = self.client.get(self.logout_url)
    self.assertRedirects(self.logout_response, self.top_url)
    

class HomeTest(TestCase):
  def setUp(self):
    self.home_url = reverse('home')
    self.login_url = reverse('login')
  
  def test_home_without_login(self):
    self.home_response = self.client.get(self.home_url)
    self.assertEqual(self.home_response.status_code, 302)


