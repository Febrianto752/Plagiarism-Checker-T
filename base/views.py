from django.shortcuts import redirect, render 
from django.views.generic import View 

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
    
    return render(self.request, self.template_name, self.context)
  
class ErrorPage(View):
  template_name = 'error-404-monochrome.svg'
  
  def get(self, *args, **kwargs):
    
    return render(self.request, self.template_name)