from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.Start.as_view(),name='start'),
    path('signup',views.Signup.as_view(),name='signup'),
]