from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('menu/', include('viewwork.urls')),
    path('app/', include('tests.testapp.urls')),
    path('app1/', include('tests.test_apps.app1.urls')),
    path('app2/', include('tests.test_apps.app2.urls')),
]
