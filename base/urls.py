from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import LandingPage, ErrorPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing_page'),
    path('error/', ErrorPage.as_view(), name='error_page'),
    path('administrator/', include(('administrator.urls', 'administrator'), namespace='administrator')),
    path('mahasiswa/', include(('mahasiswa.urls', 'mahasiswa'), namespace='mahasiswa')),
    path('plagiarisme/', include(('plagiarisme.urls', 'plagiarisme'), namespace='plagiarisme'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)