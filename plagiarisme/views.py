from django.shortcuts import render
from mahasiswa.models import Mahasiswa
from django.views.generic import DetailView, View
# Create your views here.

# === Tampilan Halaman ===
class CekPlagiarisme(View):
  template_name = 'plagiarisme/cek_plagiarisme.html'
  context = {
    'title': 'cek plagiarisme'
  }
  
  def get(self, *args, **kwargs):
    object = Mahasiswa.objects.get(npm=kwargs['npm'])
    self.context['object'] = object
    return render(self.request, self.template_name, self.context)
    
  
  
  
  
  
  
  
  
  
  
# == Process ==

 