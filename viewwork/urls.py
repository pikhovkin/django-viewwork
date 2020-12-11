from django.urls import path
from django.contrib.auth.views import logout_then_login

from viewwork.views import menu


urlpatterns = [
    path('', menu),
    path('logout/', logout_then_login, name='vw_logout'),
]
