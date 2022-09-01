from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('accounts', include('django.contrib.auth.urls')),
    path('home', views.HomeView.as_view(), name='home'),
    path('tweet', views.TweetView.as_view(), name='tweet'),
    path('<int:pk>/delete', views.DeleteTweetView.as_view(), name='delete'),
    path('profile/<slug:name>', views.ProfileView.as_view(), name='profile'),
    path('update/<int:pk>', views.AccountUpdateView.as_view(), name='update'),
    path('follow/<slug:name>', views.FollowView.as_view(), name='follow'),
    path('unfollow/<slug:name>', views.UnFollowView.as_view(), name='unfollow'),
    path('followlist/<slug:name>', views.FollowListView.as_view(), name='followlist'),
    path('followerlist/<slug:name>', views.FollowerListView.as_view(), name='followerlist'),
]
