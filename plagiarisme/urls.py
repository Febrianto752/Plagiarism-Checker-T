from django.urls import path
from .views import CekPlagiarisme

urlpatterns = [
  path('mahasiswa/<str:npm>/', CekPlagiarisme.as_view(), name='cek_plagiarisme')
]
