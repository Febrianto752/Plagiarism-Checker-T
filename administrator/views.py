from django.shortcuts import redirect, render
from django.views.generic import View 
from .models import Admin
from django.contrib import messages
from django.urls import reverse
# Create your views here.

class Login(View):
  template_name = 'auth/admin/login.html'
  context = {
    'title': 'login admin'
  }
  
  def get(self, *args, **kwargs):
    if 'username' in self.request.session:
      return redirect('administrator:dashboard')
    else:
      self.request.session.flush()
      
    return render(self.request, self.template_name, self.context)
  
  
  def post(self, *args, **kwargs):
    username = self.request.POST['username']
    password = self.request.POST['password']
    
    user = Admin.objects.filter(username=username, password=password)
    if user.exists():
      self.request.session['username'] = username
      return redirect('administrator:dashboard')
    else:
      messages.error(self.request, 'your username or password is wrong!!')
      return redirect('administrator:login')


class Dashboard(View):
  template_name = 'admin/dashboard.html'
  context = {
    'title': 'dashboard'
  }
  
  def get(self, *args, **kwargs):
    if not 'username' in self.request.session:
      return redirect('/')
    
    return render(self.request, self.template_name, self.context)


class Profile(View):
  template_name = 'admin/profile.html'
  context = {
    'title': 'profile'
  }
  
  
  def get(self, *args, **kwargs):
    return render(self.request, self.template_name, self.context)