from django.urls import path, include

from .views import page


urlpatterns = [
    path('page/', page, name='test_app_page')
]
