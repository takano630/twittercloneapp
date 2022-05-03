from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate

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
  queryset = Tweet.objects.order_by('published_at').reverse()
  context_object_name = "tweet_list"
  template_name = 'user/home.html'


class TweetView(LoginRequiredMixin, CreateView):
  model = Tweet
  fields = ['text']
  template_name = "user/tweet.html"

  def post(self, request):
    self.form = TweetCreateForm(request.POST)
    if self.form.is_valid():
      tweet = self.form.save(commit=False)
      tweet.user = request.user      
      tweet.save()
      return redirect('home')
    else:
      return redirect('tweet')



class DeleteTweetView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
  model = Tweet
  success_url = reverse_lazy('home')

  def test_func(self):
    pk = self.kwargs["pk"]
    tweet = Tweet.objects.get(pk=pk)
    return tweet.user == self.request.user

  def handle_no_permission(self):
    return redirect('home')
