from django.shortcuts import render, redirect
from .models import Mahasiswa 
from django.views.generic import ListView, View
from django.contrib import messages
# Create your views here.


JURUSAN_JURUSAN = [
  'Informatika'
]


class DaftarMahasiswa(ListView):
  template_name = 'mahasiswa/daftar_mahasiswa.html'
  model = Mahasiswa
  paginate_by = 25
  
  def get(self, *args, **kwargs):
    if not 'username' in self.request.session:
      return redirect('/')
    
    return super().get(*args, **kwargs)
  
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data()
    context['title'] = 'daftar mahasiswa'
    return context
  
  
class Tambah(View):
  template_name = 'mahasiswa/tambah.html'
  context = {
    'title': 'tambah mahasiswa'
  }
  
  
  def get(self, *args, **kwargs):
    if not 'username' in self.request.session:
      return redirect('/')
    
    self.context['jurusan_jurusan'] = JURUSAN_JURUSAN
    
    return render(self.request, self.template_name, self.context)
  
  
  def post(self, *args, **kwargs):
    npm = self.request.POST['npm']
    nama = self.request.POST['nama']
    password = self.request.POST['password']
    email = self.request.POST['email']
    jurusan = self.request.POST['jurusan']
    semester = self.request.POST['semester']
    no_telp = self.request.POST['no_telp']
    
    try:
      Mahasiswa.objects.create(npm=npm, nama=nama, email=email, password=password, jurusan=jurusan, semester=semester, no_telp=no_telp)
    except:
      messages.error(self.request, 'something error')
      return redirect('mahasiswa:daftar_mahasiswa')
    
    messages.success(self.request, f'Berhasil membuat mahasiswa baru dengan npm {npm}')
    return redirect('mahasiswa:daftar_mahasiswa')