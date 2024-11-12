from django.urls import path
from djangoapp.views import auth

urlpatterns = [
    path('login', auth.login),
    path('register', auth.register),
    path('test', auth.test),
]