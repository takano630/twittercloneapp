from asyncio.windows_events import NULL
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AccountCreateForm

class TopView(TemplateView):
  template_name = 'top.html'


class SignupView(CreateView):
    form_class = AccountCreateForm
    template_name = "user/signup.html" 
    
    def form_valid(self, form):
      user = form.save() 
      return render(self.request, 'user/signup_successed.html') 


class HomeView(LoginRequiredMixin, TemplateView):
  template_name = 'user/home.html'

