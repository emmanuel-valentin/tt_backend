from django.urls import path
from djangoapp.views import registerView, loginView

urlpatterns = [
    path('register', registerView.register),
    path('login', loginView.login),
]