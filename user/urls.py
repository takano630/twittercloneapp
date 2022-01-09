from django.urls import path

from . import views

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('signup', views.SignupView.as_view(), name='signup'),
]
