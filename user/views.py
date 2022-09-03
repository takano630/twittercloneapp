from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate

from .forms import AccountCreateForm, ProfileForm, TweetCreateForm
from .models import Tweet, Account, FollowRelationship

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
  form_class = TweetCreateForm
  template_name = "user/tweet.html"

  def form_valid(self, form):
    tweet = form.save(commit = False)
    tweet.user = self.request.user      
    tweet.save()
    return redirect('home')


class DeleteTweetView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
  model = Tweet
  success_url = reverse_lazy('home')

  def test_func(self):
    tweet = self.get_object()
    return tweet.user == self.request.user

  def handle_no_permission(self):
    return redirect('home')


class ProfileView(TemplateView):
  model = Account
  template_name = 'user/profile.html'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    user_profile = get_object_or_404(Account, username = self.kwargs['name'])
    user_follow = FollowRelationship.objects.filter(follower = user_profile)
    context['username'] = user_profile.username
    context['email'] = user_profile.email
    context['age'] = user_profile.age
    context['following_number'] = user_follow.count()
    context['followee_number'] = user_profile.followed.all().count()
    return context

  def post(self, *args, **kwargs):
    user_profile = get_object_or_404(Account, username = self.kwargs['name'])
    my_follow = FollowRelationship.objects.filter(follower = self.request.user, followee = user_profile)
    if my_follow.exists():
      return redirect('unfollow', name = user_profile.username)
    else:
      return redirect('follow', name = user_profile.username)


class AccountUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
  model = Account
  template_name = 'user/update.html'
  form_class = ProfileForm
  success_url = reverse_lazy('home')

  def test_func(self):
    self.user = self.get_object()
    return self.user.username == self.request.user.username

  def handle_no_permission(self):
    return redirect('profile', name = self.user.username)


class FollowView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    follow_user = get_object_or_404(Account, username = self.kwargs['name'])
    user = request.user
    
    if follow_user.username == user.username:
      pass
    else:
      FollowRelationship.objects.get_or_create(follower = user, followee = follow_user)
    return redirect('profile', name = follow_user.username)


class UnFollowView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    unfollow_user = get_object_or_404(Account, username = self.kwargs['name'])
    user = request.user
    
    if unfollow_user.username == user.username:
      pass
    else:
      FollowRelationship.objects.get(follower = user, followee = unfollow_user).delete()
    return redirect('profile', name = unfollow_user.username)


class FollowListView(LoginRequiredMixin, ListView):
  template_name = 'user/followlist.html'
  context_object_name = 'follower_list'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    user_profile = get_object_or_404(Account, username = self.kwargs['name'])
    context['username'] = user_profile.username
    return context

  def get_queryset(self, *args, **kwargs):
    user = get_object_or_404(Account, username = self.kwargs['name'])
    my_follow = FollowRelationship.objects.filter(follower = user)
    return my_follow

  
class FollowerListView(LoginRequiredMixin, ListView):
  template_name = 'user/followerlist.html'
  context_object_name = 'followee_list'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    user_profile = get_object_or_404(Account, username = self.kwargs['name'])
    context['username'] = user_profile.username
    return context

  def get_queryset(self, *args, **kwargs):
    user = get_object_or_404(Account, username = self.kwargs['name'])
    return user.followed.prefetch_related("follower").all()

