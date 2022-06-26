from django.urls import path 
from .views import DaftarMahasiswa


urlpatterns = [
  path('', DaftarMahasiswa.as_view(), name='daftar_mahasiswa')
]