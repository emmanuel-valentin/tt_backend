from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

def iniciar_sesion(data):
    user = authenticate(username=data["email"], password=data["password"])
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token), str(refresh)
    return None, None