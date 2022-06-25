from django.urls import path 
from .views import Login, Dashboard, Profile

urlpatterns = [ 
  path('', Login.as_view(), name='login'),
  path('dashboard/', Dashboard.as_view(), name='dashboard'),
  path('profile/', Profile.as_view(), name='profile')
]