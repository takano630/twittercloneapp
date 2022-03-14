from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Account, Tweet

class AccountCreateForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2', 'age')


class TweetCreateForm(forms.ModelForm):


    class Meta():
        model = Tweet
        fields = ('user', 'text', 'published_date',)
