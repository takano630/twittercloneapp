from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
    path('home', views.HomeView.as_view(), name='home'),
    path('login',include('django.contrib.auth.urls')),
    path('logout',include('django.contrib.auth.urls')),
]
