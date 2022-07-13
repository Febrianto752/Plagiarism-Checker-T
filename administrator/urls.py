from django.urls import path 
from .views import BuatAdminPertama, DaftarAdmin, Hapus, HapusDataTraining, Login, Dashboard, Profile, TambahAdmin, DataTrainings, TambahDataTraining, Logout, UbahPassword, UbahProfile, UbahDataTraining

urlpatterns = [ 
  path('', Login.as_view(), name='login'),
  path('logout/', Logout.as_view(), name='logout'),
  path('dashboard/', Dashboard.as_view(), name='dashboard'),
  path('profile/', Profile.as_view(), name='profile'),
  path('daftar_admin/', DaftarAdmin.as_view(), name='daftar_admin'),
  path('tambah/', TambahAdmin.as_view(), name='tambah'),
  path('hapus/<str:username>', Hapus.as_view(), name='hapus'),
  path('data_trainings/', DataTrainings.as_view(), name='data_trainings'),
  path('tambah_data_training/', TambahDataTraining.as_view(), name='tambah_data_training'),
  path('hapus_data_trainings/<str:id>/', HapusDataTraining.as_view(), name='hapus_data_training'),
  path('ubah_data_training/<str:id>/', UbahDataTraining.as_view(), name='ubah_data_training'),
  path('ubah_profile/<str:username>/', UbahProfile.as_view(), name='ubah_profile'),
  path('ubah_password/', UbahPassword.as_view(), name='ubah_password'),
  path('buat_admin_pertama/', BuatAdminPertama.as_view(), name='buat_admin_pertama'),

]