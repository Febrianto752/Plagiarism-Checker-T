from django.shortcuts import redirect, render
from django.views.generic import View, ListView, RedirectView, DetailView

from administrator.forms import DataTrainingForm
from .models import Admin, DataTraining
from django.contrib import messages
from django.urls import reverse, resolve

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

class Logout(RedirectView):
  url = '/administrator'
  
  def get_redirect_url(self, *args, **kwargs):
    self.request.session.flush()
    return super().get_redirect_url(*args, **kwargs)
  
class Dashboard(View):
  template_name = 'admin/dashboard.html'
  context = {
    'title': 'dashboard'
  }
  
  def get(self, *args, **kwargs):
    if not 'username' in self.request.session:
      return redirect('/')
    
    
    current_url = resolve(self.request.path_info).url_name
    self.context['current_url'] = current_url
    
    
    return render(self.request, self.template_name, self.context)


class Profile(View):
  template_name = 'admin/profile.html'
  context = {
    'title': 'profile'
  }
  
  
  def get(self, *args, **kwargs):
    if not 'username' in self.request.session:
      return redirect('/')
    
    current_url = resolve(self.request.path_info).url_name
    self.context['current_url'] = current_url
    
    profile = Admin.objects.get(username=self.request.session['username'])
    self.context['profile'] = profile
    
    return render(self.request, self.template_name, self.context)
  
  
class DaftarAdmin(ListView):
  template_name = 'admin/daftar_admin.html'
  model = Admin 
  paginate_by = 25
  
  def get(self, *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('/')
    
    
    
    return super().get(*args, **kwargs)
  
  def get_context_data(self, *args, **kwargs):
    current_url = resolve(self.request.path_info).url_name
    
    context = super().get_context_data()
    context['title'] = 'daftar damin'
    context['current_url'] = current_url
    return context


class TambahAdmin(View):
  template_name = 'admin/tambah.html'
  
  def get(self,  *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('administrator:login')
    
    context = {
      'title': 'Tambah Admin'
    }
    
    return render(self.request, self.template_name, context)
  
  
  def post(self, *args, **kwargs):
    username = self.request.POST['username']
    password = self.request.POST['password']
    nama = self.request.POST['nama']
    email = self.request.POST['email']
    no_telp = self.request.POST['no_telp']
    
    
    try:
      Admin.objects.create(username=username,nama=nama, password=password, email=email, no_telp=no_telp)
    except:
      messages.error(self.request,'Something Error')
      return redirect('administrator:tambah')
    
    messages.success(self.request, 'berhasil menambah admin baru')
    return redirect('administrator:daftar_admin')


class Hapus(View):
  def post(self, *args, **kwargs):
    Admin.objects.get(username=kwargs['username']).delete()
    messages.success(self.request, 'berhasil menghapus admin dengan username = '+ kwargs['username'])
    return redirect('administrator:daftar_admin')


class UbahProfile(View):
  template_name = 'admin/ubah_profile.html'
  context = {
    'title': 'ubah profile admin'
  }
  
  def get(self, *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('/')
    
    admin = Admin.objects.get(username=self.request.session['username'])
    self.context['admin'] = admin
    return render(self.request, self.template_name, self.context)
  
  def post(self, *args, **kwargs):
    nama = self.request.POST['nama']
    email = self.request.POST['email']
    no_telp = self.request.POST['no_telp']
    
    Admin.objects.filter(username=kwargs['username']).update(nama=nama, email=email, no_telp=no_telp)
    messages.success(self.request, 'berhasil mengubah profile')
    return redirect('administrator:profile')
  

class UbahPassword(View):
  template_name = 'admin/ubah_password.html'
  context = {
    'title': 'ubah password'
  }
  
  def get(self, *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('/error')
    
    return render(self.request, self.template_name, self.context)

  def post(self, *args, **kwargs):
    password = self.request.POST['password']
    confirm_password = self.request.POST['confirm_password']
    
    if password != confirm_password:
      messages.error(self.request, 'password and confirm password dont match!')
      return redirect('administrator:ubah_password')
    
    Admin.objects.filter(username=self.request.session['username']).update(password=password)
    messages.success(self.request, 'berhasil mengubah password akun')
    return redirect('administrator:profile')


class BuatAdminPertama(View):
  template_name = 'admin/buat_admin_pertama.html'
  extra_context = {
    'title': 'create first admin'
  }
  
  def get(self, *args, **kwargs):
    return render(self.request, self.template_name, self.extra_context)






# ===== Data Trainings =====
class DataTrainings(ListView):
  template_name = 'admin/data_trainings.html'

  model = DataTraining
  paginate_by = 25
  
  def get(self, *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('administrator:login')

    
    return super().get(*args, **kwargs)
  
  def get_context_data(self, *args, **kwargs):
    current_url = resolve(self.request.path_info).url_name
    context = super().get_context_data()
    context['title'] = 'daftar data training'
    context['current_url'] = current_url
    return context
  

class TambahDataTraining(View):
  template_name = 'admin/tambah_data_training.html'
  context = {
     'title': 'Tambah Data Training'
  }
  
  def get(self,  *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('administrator:login')
    
    data_training_form = DataTrainingForm()
    self.context['data_training_form'] = data_training_form

    return render(self.request, self.template_name, self.context)
  
  
  def post(self, *args, **kwargs):
    form = DataTrainingForm(self.request.POST, self.request.FILES)
    
    if form.is_valid():
      try:
        form.save()
        
      except:
        messages.error(self.request, 'file yang anda upload harus pdf...') # mengirimkan flash message error
        return redirect('administrator:tambah_data_training')
      
      messages.success(self.request, 'Berhasil Mengupload...')
      return redirect('administrator:data_trainings')

class HapusDataTraining(View):
  def post(self, *args, **kwargs):
    DataTraining.objects.get(id=kwargs['id']).delete()
    messages.success(self.request, 'berhasil menghapus data training')
    
    return redirect('administrator:data_trainings')


class UbahDataTraining(View):
  template_name = 'admin/ubah_data_training.html'
  context = {
    'title': 'ubah detail data training'
  }
  
  def get(self, *args, **kwargs):
    data_training = DataTraining.objects.get(id=kwargs['id'])
    self.context['data_training'] = data_training
    return render(self.request, self.template_name, self.context)
  
  def post(self, *args, **kwargs):
    id = kwargs['id']
    
    judul = self.request.POST['judul']
    penulis = self.request.POST['penulis']
    tahun = self.request.POST['tahun']
    
    try:
      data_training = DataTraining.objects.filter(id=id)
      data_training.update(judul=judul, penulis=penulis, tahun=tahun)
      messages.success(self.request, 'berhasil mengubah detail data training')
      return redirect('administrator:data_trainings')
    except:
      messages.error(self.request, 'something error')
      return redirect('administrator:ubah_data_training', id)
  
  












