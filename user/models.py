from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Account(AbstractUser):
  email = models.EmailField(blank=False, max_length=254, verbose_name='email address')
  age = models.PositiveSmallIntegerField(null=True,blank=True)
  

class Tweet(models.Model):
  user = models.ForeignKey('Account', on_delete=models.CASCADE, blank=True)
  text = models.CharField(max_length=200)
  published_date = models.DateTimeField(default=timezone.now, blank=True)
