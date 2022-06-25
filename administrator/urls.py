from django.urls import path 
from .views import DaftarAdmin, Login, Dashboard, Profile, TambahAdmin

urlpatterns = [ 
  path('', Login.as_view(), name='login'),
  path('dashboard/', Dashboard.as_view(), name='dashboard'),
  path('profile/', Profile.as_view(), name='profile'),
  path('daftar_admin/', DaftarAdmin.as_view(), name='daftar_admin'),
  path('tambah_admin', TambahAdmin.as_view(), name='tambah')
]