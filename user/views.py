from pickle import TRUE
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.utils import timezone

from .forms import AccountCreateForm, TweetCreateForm
from .models import Tweet

class TopView(TemplateView):
  template_name = 'top.html'


class SignupView(CreateView):
    form_class = AccountCreateForm
    template_name = "user/signup.html" 
    
    def form_valid(self, form):
      user = form.save() 
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(self.request, user)
      return redirect('home')


class HomeView(LoginRequiredMixin, ListView):
  model = Tweet
  queryset = Tweet.objects.order_by('published_date').reverse()
  context_object_name = "tweet_list"
  template_name = 'user/home.html'


class TweetView(LoginRequiredMixin, CreateView):
  model = Tweet
  fields = ['text']
  template_name = "user/tweet.html"

  def post(self,request):
    self.form = TweetCreateForm(request.POST)
    if self.form.is_valid():
      tweet = self.form.save(commit=False)
      tweet.user = request.user
      tweet.published_date = timezone.now()
      tweet.save()
      return redirect('home')
    else:
      return redirect('tweet')

      