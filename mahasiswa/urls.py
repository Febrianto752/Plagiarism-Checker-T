from django.urls import path 
from .views import DaftarMahasiswa, Tambah, Profile, UbahProfile


urlpatterns = [
  path('', DaftarMahasiswa.as_view(), name='daftar_mahasiswa'),
  path('tambah/', Tambah.as_view(), name='tambah'),
  path('profile/<str:npm>/', Profile.as_view(), name='profile'),
  path('ubah/<str:npm>/', UbahProfile.as_view(), name='ubah_profile'),
]