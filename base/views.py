from django.shortcuts import redirect, render 
from django.views.generic import View 
from django.urls import resolve
class LandingPage(View):
  template_name = 'landing_page.html'
  context = {
    'title': 'landing page'
  }
  def get(self, *args, **kwargs):
    if 'username' in self.request.session:
      return redirect('administrator:dashboard')
    elif 'npm' in self.request.session:
      return redirect('mahasiswa:dashboard')
    
    
    current_url = resolve(self.request.path_info).url_name
    print(current_url)
    
    return render(self.request, self.template_name, self.context)
  
class ErrorPage(View):
  template_name = 'error-404-monochrome.svg'
  
  def get(self, *args, **kwargs):
    
    return render(self.request, self.template_name)