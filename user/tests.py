from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Account, Tweet
from twittercloneapp.settings import LOGIN_REDIRECT_URL

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
    self.home_url = reverse('home')

  def test_user_creation(self):
    self.assertTrue(Account.objects.exists())
    self.assertRedirects(self.response, self.home_url)



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
    self.login_url = reverse('login')

  def test_login_success(self):
    login_data = {'username':'people', 'password':'testpassword'}
    login_response = self.client.post(self.login_url, login_data)
    self.assertRedirects(login_response, LOGIN_REDIRECT_URL)


class LoginFailTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    self.login_url = reverse('login')
  
  def test_mistake_password(self):
    login_data = {'username':'people', 'password':'mistakepassword'}
    login_response = self.client.post(self.login_url, login_data)
    self.assertEqual(login_response.status_code, 200)

  def test_not_exist_user(self):
    login_data = {'username':'no_people', 'password':'testpassword'}
    login_response = self.client.post(self.login_url, login_data)
    self.assertEqual(login_response.status_code, 200)


class LogoutTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    self.top_url = reverse('top')
    self.client.login(username='people', password='testpassword')

  def test_logout(self):
    logout_url = reverse('logout')
    logout_response = self.client.get(logout_url)
    self.assertRedirects(logout_response, self.top_url)
    

class HomeSuccessTest(TestCase):
  def setUp(self):
    testpeople = Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    Tweet.objects.create(user = testpeople, text = 'testtest', published_at = timezone.now())
    self.home_url = reverse('home')
    self.client.login(username='people', password='testpassword')


  def test_home_succese(self):
    home_response = self.client.get(self.home_url)
    self.assertEqual(home_response.status_code, 200)
  
  def test_succese_get_tweet(self):
    home_response = self.client.get(self.home_url)
    self.assertQuerysetEqual(home_response.context["object_list"], ['<Tweet: Tweet object (1)>'])

class HomeFailTest(TestCase):
  def setUp(self):
    self.home_url = reverse('home')

  def test_home_without_login(self):
    home_response = self.client.get(self.home_url)
    self.assertEqual(home_response.status_code, 302)


class TweetSuccessTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    self.client.login(username='people', password='testpassword')
    self.tweet_url = reverse('tweet')
    self.tweet_data = {'text':'test'}
    self.home_url = reverse('home')

  def test_succese_get(self):
    self.response = self.client.get(self.tweet_url)
    self.assertEqual(self.response.status_code, 200)

  def test_tweet_success(self):
    self.tweet_response = self.client.post(self.tweet_url, self.tweet_data)
    self.assertEqual(self.tweet_response.status_code, 302)
    self.assertRedirects(self.tweet_response, self.home_url)
    self.assertEqual(Tweet.objects.count(), 1)
  

class TweetFailTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    self.tweet_url = reverse('tweet')

  def test_tweet_fail(self):
    self.client.login(username='people', password='testpassword')
    tweet_data = {'text':''}
    tweet_response = self.client.post(self.tweet_url, tweet_data)
    self.assertRedirects(tweet_response, self.tweet_url)
    self.assertEqual(Tweet.objects.count(), 0)

  def test_tweet_without_login(self):
    tweet_get_response = self.client.get(self.tweet_url)
    self.assertEqual(tweet_get_response.status_code, 302)


class TweetDeleteSuccessTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    self.tweet_url = reverse('tweet')
    self.tweet_data = {'text':'test'}
    self.home_url = reverse('home')
    self.client.login(username='people', password='testpassword')
    self.client.post(self.tweet_url, self.tweet_data)
    self.tweet_delete_url = '/1/delete'
  
  def test_tweet_delete(self):
    self.tweet_delete_response = self.client.post(self.tweet_delete_url, {"delete":"delete"})
    self.assertRedirects(self.tweet_delete_response, self.home_url)

  def test_tweet_delete_count(self):
    self.client.post(self.tweet_delete_url, {"delete":"delete"})
    self.assertEqual(Tweet.objects.count(), 0)

class TweetDeleteFailTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword', age='1')
    Account.objects.create_user(username='differentuser', email='test@test.test', password='testpassword', age='2')
    self.tweet_url = reverse('tweet')
    self.tweet_data = {'text':'test'}
    self.home_url = reverse('home')
    self.client.login(username='people', password='testpassword')
    self.client.post(self.tweet_url, self.tweet_data)
    self.tweet_delete_url = '/1/delete'

  def test_failure_post_with_not_exist_tweet(self):
    self.tweet_delete_not_exist_url = '/2/delete/'
    self.tweet_delete_not_exist_response = self.client.post(self.tweet_delete_not_exist_url, {"delete":"delete"})
    self.assertEqual(self.tweet_delete_not_exist_response.status_code, 404)    

  def test_failure_post_with_incorrect_user(self):
    self.client.login(username='differentuser', password='testpassword')
    self.tweet_delete_response = self.client.post(self.tweet_delete_url, {"delete":"delete"})
    self.assertRedirects(self.tweet_delete_response, self.home_url)

 
class ProfileTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword',age='1')
    Account.objects.create_user(username='differentpeople', email='test@test.test', password='testpassword',age='1')
    self.profile_url = '/profile/people'
    self.profile_different_url = '/profile/differentpeople'

  def test_succese_get(self):
    self.client.login(username='people', password='testpassword')
    self.response = self.client.get(self.profile_url)
    self.assertEqual(self.response.status_code, 200)

  def test_different_user_profile(self):
    self.client.login(username='people', password='testpassword')
    self.response = self.client.get(self.profile_different_url)
    self.assertEqual(self.response.status_code, 200)

  
class ProfileFailureTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword',age='1')
    self.profile_url = '/profile/people/'

  def test_not_login(self):
    self.response = self.client.get(self.profile_url)
    self.assertEqual(self.response.status_code, 404)


class UpdateSucceseTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword',age='1')
    self.profile_url = '/profile/people'
    self.update_url = '/update/1'

  def test_succese_get(self):
    self.client.login(username='people', password='testpassword')
    self.get_response = self.client.get(self.update_url)
    self.assertEqual(self.get_response.status_code, 200)

  def test_update(self):
    self.client.login(username='people', password='testpassword')
    self.update_data = {'username':'people2', 'email':'test2@test.test', 'age':'2'}
    self.update_response = self.client.post(self.update_url, self.update_data)
    self.assertEqual(self.update_response.status_code, 302)
    self.assertEqual(Account.objects.count(), 1)

class UpdateFailureTest(TestCase):
  def setUp(self):
    Account.objects.create_user(username='people', email='test@test.test', password='testpassword',age='1')
    self.profile_url = '/profile/people'
    self.update_url = '/update/1'
    self.data = {'username':'testpeople', 'email':'test@test.test', 'age':'1'}

  def test_different_user(self):
    Account.objects.create_user(username='differentpeople', email='test@test.test', password='testpassword',age='1')
    self.client.login(username='people', password='testpassword')
    self.update_different_url = '/update/2'
    self.profile_different_url = '/profile/differentpeople'
    self.response = self.client.get(self.update_different_url)
    self.assertRedirects(self.response, self.profile_different_url)

  def test_not_login(self):
    self.get_response = self.client.get(self.update_url)
    self.assertEqual(self.get_response.status_code, 302)

  def test_data_empty(self):
    empty_data = {}
    self.client.login(username='people', password='testpassword')
    self.update_response = self.client.post(self.update_url, empty_data)
    self.assertEqual(self.update_response.status_code, 200)
    self.assertEqual(Account.objects.count(), 1)
  
  def test_username_empty(self):
    self.data['username'] = ''
    self.client.login(username='people', password='testpassword')
    self.update_response = self.client.post(self.update_url, self.data)
    self.assertEqual(self.update_response.status_code, 200)
    self.assertEqual(Account.objects.count(), 1)
  
  def test_email_empty(self):
    self.data['email'] = ''
    self.client.login(username='people', password='testpassword')
    self.update_response = self.client.post(self.update_url, self.data)
    self.assertEqual(self.update_response.status_code, 200)
    self.assertEqual(Account.objects.count(), 1)
 
  def test_age_empty(self):
    self.data['age'] = ''
    self.client.login(username='people', password='testpassword')
    self.update_response = self.client.post(self.update_url, self.data)
    self.assertEqual(self.update_response.status_code, 200)
    self.assertEqual(Account.objects.count(), 1)

