from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import AccountCreatForm
from django.views.generic import TemplateView

class StartView(TemplateView):
  template_name = 'start.html'

class SignupView(CreateView):
    form_class = AccountCreatForm
    template_name = "user_HTML/signup.html" 
    def form_valid(self, form):
      user = form.save() 
      return render(self.request,'user_HTML/successed_signup.html') 
