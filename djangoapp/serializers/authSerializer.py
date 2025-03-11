from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class RegisterSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=True)
    apellidoPaterno = serializers.CharField(required=True)
    apellidoMaterno = serializers.CharField(required=True)
    fechaNacimiento = serializers.DateField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    nacionalidad = serializers.CharField(required=True)
    telefono = serializers.CharField(required=True)
    cedula = serializers.CharField(required=False)
