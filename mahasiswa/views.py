from django.shortcuts import render, redirect
from .models import Mahasiswa 
from django.views.generic import ListView, View
# Create your views here.

class DaftarMahasiswa(ListView):
  template_name = 'mahasiswa/daftar_mahasiswa.html'
  model = Mahasiswa
  paginate_by = 25
  context = {
    'title': 'daftar mahasiswa'
  }
  
  def get(self, *args, **kwargs):
    
    return render(self.request, self.template_name, self.context)
  
class Tambah(View):
  template_name = 'mahasiswa/tambah.html'
  context = {
    'title': 'tambah mahasiswa'
  }
  
  def get(self, *args, **kwargs):
    if 'username' in self.request.session:
      return redirect('/')
  