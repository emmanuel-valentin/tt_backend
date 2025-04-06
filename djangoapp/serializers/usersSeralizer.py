from rest_framework import serializers
from djangoapp.models import Fisioterapeuta, Persona, User


class PersonaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    fecha = serializers.DateField(required=False)
    telefono = serializers.CharField(required=False)
    foto_url = serializers.CharField(required=False)

    class Meta:
        model = Persona
        fields = ['id', 'fecha', 'nacionalidad', 'telefono', 'foto_url']

class UsuarioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class FisioterapeutaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    cedula = serializers.CharField(required=False)
    codigo_token = serializers.CharField(required=False)
    persona = PersonaSerializer(required=False)
    usuario = UsuarioSerializer(required=False)

class PacienteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    ocupacion = serializers.CharField(required=False)
    persona = PersonaSerializer(required=False)
    usuario = UsuarioSerializer(required=False)

class LinkPatientToPhysiotherapistSerializer(serializers.Serializer):
    codigo = serializers.CharField(required=True)

class SendFeedbackSerializer(serializers.Serializer):
    ejercicio_asignado_id = serializers.IntegerField(required=True)
    feedback = serializers.CharField(required=True)