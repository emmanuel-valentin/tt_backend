from django.urls import path
from djangoapp.views import registerView, loginView

urlpatterns = [
    path('registar', registerView.register),
    path('iniciar-sesion', loginView.login),
]