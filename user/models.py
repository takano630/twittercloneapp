from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Account(AbstractUser):
  email = models.EmailField(blank=False, max_length=254, verbose_name='email address')
  age = models.PositiveSmallIntegerField(null=False, blank=False, default='0')
  

class FollowRelationship(models.Model):
   follower = models.ForeignKey('Account', on_delete=models.CASCADE)
   followee = models.ForeignKey('Account', related_name = 'followed', on_delete=models.CASCADE)


class Tweet(models.Model):
  user = models.ForeignKey('Account', on_delete=models.CASCADE)
  text = models.TextField(max_length=200)
  published_at = models.DateTimeField(default=timezone.now)
