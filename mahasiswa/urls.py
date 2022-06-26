from django.urls import path 
from .views import DaftarMahasiswa, Tambah


urlpatterns = [
  path('', DaftarMahasiswa.as_view(), name='daftar_mahasiswa'),
  path('tambah/', Tambah.as_view(), name='tambah')
]