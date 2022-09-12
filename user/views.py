from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.core.exceptions import BadRequest

from .forms import AccountCreateForm, ProfileForm, TweetCreateForm
from .models import Tweet, Account, FollowRelationship, LikeRelationship

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
  
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    user = self.request.user
    context['like_list'] = LikeRelationship.objects.filter(user = user).values_list("tweet", flat = True)
    return context


class TweetView(LoginRequiredMixin, CreateView):
  model = Tweet
  form_class = TweetCreateForm
  template_name = "user/tweet.html"

  def form_valid(self, form):
    tweet = form.save(commit = False)
    tweet.user = self.request.user      
    tweet.save()
    return redirect('home')


class DetailTweetView(LoginRequiredMixin, TemplateView):
  template_name = "user/tweet_detail.html"

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    user = self.request.user
    tweet_detail = get_object_or_404(Tweet, pk = self.kwargs['pk'])
    context['tweet'] = tweet_detail
    context['like_number'] = LikeRelationship.objects.filter(tweet = tweet_detail).count()
    return context


class DeleteTweetView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
  model = Tweet
  success_url = reverse_lazy('home')

  def test_func(self):
    tweet = self.get_object()
    return tweet.user == self.request.user

  def handle_no_permission(self):
    return redirect('home')


class ProfileView(ListView):
  model = Account
  template_name = 'user/profile.html'
  context_object_name = "tweet_list"

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    user_profile = get_object_or_404(Account, username = self.kwargs['name'])
    user_follow = FollowRelationship.objects.filter(follower = user_profile)
    context['username'] = user_profile.username
    context['email'] = user_profile.email
    context['age'] = user_profile.age
    context['following_number'] = user_follow.count()
    context['followee_number'] = user_profile.followed.all().count()
    context['is_follow'] = FollowRelationship.objects.filter(follower = self.request.user, followee = user_profile).exists()
    return context

  def get_queryset(self, *args, **kwargs):
    user = get_object_or_404(Account, username = self.kwargs['name'])
    return Tweet.objects.filter(user = user).order_by('published_at').reverse()


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
  def post(self, request, *args, **kwargs):
    follow_user = get_object_or_404(Account, username = self.kwargs['name'])
    user = request.user
    
    if follow_user.username == user.username:
      raise BadRequest
    else:
      FollowRelationship.objects.create(follower = user, followee = follow_user)
    return redirect('profile', name = follow_user.username)


class UnFollowView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    unfollow_user = get_object_or_404(Account, username = self.kwargs['name'])
    user = request.user
    
    if unfollow_user.username == user.username:
      raise BadRequest
    else:
      FollowRelationship.objects.filter(follower = user, followee = unfollow_user).delete()
    return redirect('profile', name = unfollow_user.username)


class FollowListView(LoginRequiredMixin, ListView):
  template_name = 'user/followlist.html'
  context_object_name = 'follow_reloationships'

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


class LikeView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    like_tweet = get_object_or_404(Tweet, pk = self.kwargs['pk'])
    user = request.user
    LikeRelationship.objects.create(tweet = like_tweet, user = user)
    return redirect('detail', pk = like_tweet.pk)


class UnLikeView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    unlike_tweet = get_object_or_404(Tweet, pk = self.kwargs['pk'])
    user = request.user
    LikeRelationship.objects.filter(tweet = unlike_tweet, user = user).delete()
    return redirect('detail', pk = unlike_tweet.pk)

