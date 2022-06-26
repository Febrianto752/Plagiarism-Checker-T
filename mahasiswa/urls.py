from django.urls import path 
from .views import DaftarMahasiswa, Tambah, Profile, UbahProfile, Hapus, Login, Dashboard


urlpatterns = [
  path('', DaftarMahasiswa.as_view(), name='daftar_mahasiswa'),
  path('login/', Login.as_view(), name='login'),
  path('dashboard/', Dashboard.as_view(), name='dashboard'),
  path('tambah/', Tambah.as_view(), name='tambah'),
  path('profile/<str:npm>/', Profile.as_view(), name='profile'),
  path('ubah/<str:npm>/', UbahProfile.as_view(), name='ubah_profile'),
  path('hapus/<str:npm>/', Hapus.as_view(), name='hapus'),
]