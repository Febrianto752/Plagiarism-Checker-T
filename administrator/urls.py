from django.urls import path 
from .views import DaftarAdmin, Hapus, HapusDataTraining, Login, Dashboard, Profile, TambahAdmin, DataTrainings, TambahDataTraining, Logout

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
  path('hapus_data_trainings/<str:id>/', HapusDataTraining.as_view(), name='hapus_data_training')

]