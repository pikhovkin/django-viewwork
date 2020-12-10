from django.urls import path

from viewwork.views import menu


urlpatterns = [
    path('', menu),
]
