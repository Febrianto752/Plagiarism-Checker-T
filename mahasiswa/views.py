from django.shortcuts import render, redirect
from administrator.models import DataTraining

from mahasiswa.forms import SkripsiForm
from .models import Mahasiswa, Skripsi 
from django.views.generic import ListView, View, DetailView, RedirectView
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
  
class Profile(DetailView):
  template_name = 'mahasiswa/profile.html'
  model = Mahasiswa 
  slug_field = 'npm'
  slug_url_kwarg = 'npm'
  
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data()
    context['title'] = 'profile'
    
    
    return context
  
class UbahProfile(View):
  template_name = 'mahasiswa/ubah.html'
  context = {
    'title': 'ubah data mahasiswa'
  }
  
  def get(self, *args, **kwargs):
    mahasiswa = Mahasiswa.objects.get(npm=kwargs['npm'])
    self.context['mahasiswa'] = mahasiswa
    
    return render(self.request, self.template_name, self.context)

class Hapus(RedirectView):
  url = '/mahasiswa/'
  
  def get_redirect_url(self, *args, **kwargs):
    Mahasiswa.objects.get(npm=kwargs['npm']).delete()
    messages.success(self.request, 'berhasil menghapus mahasiswa dengan npm = '+ kwargs['npm'])
    
    return super().get_redirect_url(*args, **kwargs)


# == for access mahasiswa == 
class Login(View):
  template_name = 'auth/mahasiswa/login.html'
  context = {
    'title': 'login'
  }
  def get(self, *args, **kwargs):
    return render(self.request, self.template_name, self.context)
     
  def post(self, *args, **kwargs):
    npm = self.request.POST['npm']
    password = self.request.POST['password']
    
    user = Mahasiswa.objects.filter(npm=npm, password=password)
    if user.exists():
      self.request.session['npm'] = npm
      return redirect('mahasiswa:dashboard')
    else:
      messages.error(self.request, 'your npm or password is wrong!!')
      return redirect('mahasiswa:login')


class Logout(RedirectView):
  url = '/mahasiswa/login'
  
  def get_redirect_url(self, *args, **kwargs):
    self.request.session.flush()
    return super().get_redirect_url(*args, **kwargs)
  
class Dashboard(View):
  template_name = 'mahasiswa/dashboard.html'
  context = {
    'title': 'dashboard'
  }
  
  def get(self, *args, **kwargs):
    if not 'npm' in self.request.session:
      return redirect('/mahasiswa/login')
    
    return render(self.request, self.template_name, self.context)

class CekPlagiarisme(DetailView):
  template_name = 'mahasiswa/cek_plagiarisme.html'
  model = Mahasiswa
  slug_field = 'npm'
  slug_url_kwarg = 'npm'
  
  def get(self, *args, **kwargs):
    if not 'npm' in self.request.session:
      return redirect('/mahasiswa/login/')
    return super().get(*args, **kwargs)
  
  def get_context_data(self,*args, **kwargs):
    jumlah_data_training = DataTraining.objects.all().count()
    context = super().get_context_data(**kwargs) 
    context['title'] = 'cek plagiarisme'
    context['jumlah_data_training'] = jumlah_data_training
    return context
  
  
class UploadSkripsi(View):
  template_name = 'mahasiswa/upload_skripsi.html'
  # context = {
  #   'title': 'upload skripsi'
  # }
  
  def get(self, request, *args, **kwargs):
    if 'npm' not in request.session:
      return redirect('mahasiswa:login')
    
    mahasiswa = Mahasiswa.objects.get(npm=kwargs['npm'])
    
    skripsi_form = SkripsiForm()
    context = {
      'title': 'upload skripsi',
      'mahasiswa': mahasiswa,
      'skripsi_form': skripsi_form,
    }

    return render(request, self.template_name, context)

  def post(self, *args, **kwargs):

    mahasiswa = Mahasiswa.objects.get(npm=self.request.POST['npm'])
    skripsi_mahasiswa = Skripsi.objects.filter(mahasiswa_id=mahasiswa.id)

    if skripsi_mahasiswa.exists():
      form = SkripsiForm(self.request.POST, self.request.FILES, instance=Skripsi.objects.get(mahasiswa_id=mahasiswa.id))
    else:
      form = SkripsiForm(self.request.POST, self.request.FILES)
    
    if form.is_valid():
      try:
        form.save()
        
      except:
        messages.error(self.request, 'file yang anda upload harus pdf...') # mengirimkan flash message error
        return redirect('mahasiswa:upload_skripsi', self.request.POST['npm'])
      
      messages.success(self.request, 'Berhasil Mengupload...')
      return redirect('mahasiswa:upload_skripsi', self.request.POST['npm'])
    
class ShowReport(View):
  template_name = 'mahasiswa/report.html'
  
  
  def get(self, *args, **kwargs):
    if 'npm' not in self.request.session:
      return redirect('mahasiswa:login')
    
    mahasiswa = Mahasiswa.objects.get(npm=kwargs['npm'])
    skripsi_mhs = Skripsi.objects.get(mahasiswa_id = mahasiswa.id)
    
    
    context = {
      'title' : 'report check plagiarism',
      'content_skripsi':skripsi_mhs.content.replace('?',''),
      'mahasiswa': mahasiswa,
      'npm': kwargs['npm']
    }
    
    return render(self.request, self.template_name, context)