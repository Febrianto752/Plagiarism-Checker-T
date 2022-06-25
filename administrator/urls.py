from django.urls import path 
from .views import Login, Dashboard

urlpatterns = [ 
  path('', Login.as_view(), name='login'),
  path('dashboard/', Dashboard.as_view(), name='dashboard')
]