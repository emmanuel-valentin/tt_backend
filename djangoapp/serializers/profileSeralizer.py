from rest_framework import serializers
from djangoapp.models import Fisioterapeuta, Persona, User


class SubirFotoDePerfilSerializer(serializers.Serializer):
    foto = serializers.FileField(required=True)