from django.shortcuts import render
from django.views.generic import View 
# Create your views here.

class Login(View):
  template_name = 'auth/admin/login.html'
  context = {
    'title': 'login admin'
  }
  def get(self, *args, **kwargs):
    return render(self.request, self.template_name, self.context)
