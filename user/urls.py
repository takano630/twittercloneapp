from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('accounts', include('django.contrib.auth.urls')),
    path('home', views.HomeView.as_view(), name='home'),
    path('tweet', views.TweetView.as_view(), name='tweet'),
    path('<int:pk>/delete', views.DeleteTweetView.as_view(), name='delete'),
]
