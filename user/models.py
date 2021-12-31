from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
  age = models.IntegerField(null=True)
  
