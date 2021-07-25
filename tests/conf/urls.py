from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include('viewwork.urls')),
    path('app/', include('tests.testapp.urls')),
]
