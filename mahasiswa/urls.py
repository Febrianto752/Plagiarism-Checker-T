from django.urls import path 
from .views import DaftarMahasiswa, ShowReport, Tambah, Profile, UbahProfile, Hapus, Login, Dashboard, CekPlagiarisme, UploadSkripsi, Logout


urlpatterns = [
  path('', DaftarMahasiswa.as_view(), name='daftar_mahasiswa'),
  path('login/', Login.as_view(), name='login'),
  path('logout/', Logout.as_view(), name='logout'),
  path('dashboard/', Dashboard.as_view(), name='dashboard'),
  
  # access admin 
  path('tambah/', Tambah.as_view(), name='tambah'),
  path('profile/<str:npm>/', Profile.as_view(), name='profile'),
  path('ubah/<str:npm>/', UbahProfile.as_view(), name='ubah_profile'),
  path('hapus/<str:npm>/', Hapus.as_view(), name='hapus'),
  # <==
  
  path('<str:npm>/cek_plagiarisme/', CekPlagiarisme.as_view(), name='cek_plagiarisme'),
  path('<str:npm>/upload/', UploadSkripsi.as_view(), name='upload_skripsi'),
  path('<str:npm>/report/', ShowReport.as_view(), name='report_plagiarism'),
]