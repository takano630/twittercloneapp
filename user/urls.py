from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.StartView.as_view(),name='start'),
    path('signup',views.SignupView.as_view(),name='signup'),
]
