from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import Accountform
from django.views.generic import TemplateView

class Start(TemplateView):
  template_name = 'start.html'

class Signup(CreateView):
    form_class = Accountform
    template_name = "User_HTML/formpage.html" 
    def form_valid(self, form):
      user = form.save() 
      return render(self.request,'User_HTML/signup.html') 
