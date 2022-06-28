from django.urls import path
from .views import CekPlagiarisme, checking, setPlagiarismPercentage, textSimiliarity

urlpatterns = [
  path('mahasiswa/<str:npm>/', CekPlagiarisme.as_view(), name='cek_plagiarisme'),
  path('<str:npm>/<str:percentage>/', setPlagiarismPercentage, name='set_plagiarism_percentage'), # API
  path('<str:npm>/<int:iteration>/<int:pk>/<int:count>', checking, name='checking'), # API
  path('report/<str:npm>/text_similiarity/', textSimiliarity, name='text_similiarity'), # API
]
