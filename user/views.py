from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import AccountCreateForm
from django.views.generic import TemplateView

class StartView(TemplateView):
  template_name = 'start.html'

class SignupView(CreateView):
    form_class = AccountCreateForm
    template_name = "user/signup.html" 
    def form_valid(self, form):
      user = form.save() 
      return render(self.request,'user/successed_signup.html') 
