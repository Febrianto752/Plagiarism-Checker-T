from django.shortcuts import redirect, render
from django.views.generic import View, ListView
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
    if not 'username' in self.request.session:
      return redirect('/')
    
    profile = Admin.objects.get(username=self.request.session['username'])
    self.context['profile'] = profile
    
    return render(self.request, self.template_name, self.context)
  
  
class DaftarAdmin(ListView):
  template_name = 'admin/daftar_admin.html'
  context = {
    'title': 'daftar admin'
  }
  model = Admin 
  paginate_by = 25
  
  def get(self, *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('administrator:login')
    
    return super().get(*args, **kwargs)
  
  def get_context_data(self, *args, **kwargs):
   
    context = super().get_context_data()
    context['title'] = 'daftar admin'
    return context
  