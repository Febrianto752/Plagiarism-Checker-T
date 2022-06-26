from django.shortcuts import redirect, render
from django.views.generic import View, ListView, RedirectView
from .models import Admin, DataTraining
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
  model = Admin 
  paginate_by = 25
  
  def get(self, *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('/')
    
    return super().get(*args, **kwargs)
  
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data()
    context['title'] = 'daftar damin'
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
      Admin.objects.create(username=username, password=password, email=email, no_telp=no_telp)
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


# ===== Data Trainings =====
class DataTrainings(ListView):
  template_name = 'admin/data_trainings.html'
  context = {
    'title': 'daftar data training'
  }
  model = DataTraining
  paginate_by = 25
  
  def get(self, *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('administrator:login')
    
    return super().get(*args, **kwargs)
  
  def get_context_data(self, *args, **kwargs):
   
    context = super().get_context_data()
    return context
  

class TambahDataTraining(View):
  template_name = 'admin/tambah_data_training.html'
  context = {
     'title': 'Tambah Data Training'
  }
  
  def get(self,  *args, **kwargs):
    if 'username' not in self.request.session:
      return redirect('administrator:login')

    return render(self.request, self.template_name, self.context)
  
  
  def post(self, *args, **kwargs):
    author = self.request.POST['author']
    tahun = self.request.POST['tahun']
    file = self.request.FILES['file']

    # try:
      # Admin.objects.create(username=username, password=password, email=email, no_telp=no_telp)
    DataTraining.objects.create(author=author, tahun=tahun, path_file=file)
    # except:
    #   messages.error(self.request,'Something Error')
    #   return redirect('administrator:tambah_data_training')
    
    messages.success(self.request, 'berhasil menambah data training baru')
    return redirect('administrator:data_trainings')

class HapusDataTraining(View):
  def post(self, *args, **kwargs):
    DataTraining.objects.get(id=kwargs['id']).delete()
    messages.success(self.request, 'berhasil menghapus data training')
    
    return redirect('administrator:data_trainings')


  
  











