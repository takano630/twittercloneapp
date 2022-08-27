from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Account, Tweet

class AccountCreateForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2', 'age')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'age')


class TweetCreateForm(forms.ModelForm):

    class Meta():
        model = Tweet
        fields = ('text',)
        
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == '':
            raise forms.ValidationError('入力されていません', code = 'empty')
        elif len(text) > 254:
            raise forms.ValidationError('文字数が多すぎます', code = 'long_content')
        return text
