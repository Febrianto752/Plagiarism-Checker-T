from django.urls import path
from .views import CekPlagiarisme, SideBySide, SideBySideView, SimiliarityBetweenTwoThesis, checking, setPlagiarismPercentage, sideBySidePlagiarismCheck, similiarityOneToOne, textSimiliarity

urlpatterns = [
  path('mahasiswa/<str:npm>/', CekPlagiarisme.as_view(), name='cek_plagiarisme'),
  path('<str:npm>/<str:percentage>/', setPlagiarismPercentage, name='set_plagiarism_percentage'), # API
  path('<str:npm>/<int:iteration>/<int:pk>/<int:count>', checking, name='checking'), # API
  path('report/<str:npm>/text_similiarity/', textSimiliarity, name='text_similiarity'), # API
  path('detail/<str:npm_mhs>/<str:id_data_training>/', SimiliarityBetweenTwoThesis.as_view(), name='detail_report'),
  path('similiarity/<str:npm_mhs>/<str:id_data_training>/', similiarityOneToOne, name='similiarity_one_to_one'), # API
  path('side_by_side/', SideBySideView.as_view(), name='side_by_side_test'),
  path('side_by_side/check/<str:inisial>', sideBySidePlagiarismCheck, name='side_by_side_check'),
]
