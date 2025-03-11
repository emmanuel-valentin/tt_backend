from rest_framework import serializers

class asignarEjercicioSerializer(serializers.Serializer):
    ejercicioID = serializers.IntegerField(required=True)
    pacienteID = serializers.IntegerField(required=True)
    fechaLimite = serializers.DateTimeField(required=True)

class actualizarEjercicioAsignadoSerializer(serializers.Serializer):
    ejercicioAsignadoID = serializers.IntegerField(required=True)
    ejercicioID = serializers.IntegerField(required=False)
    pacienteID = serializers.IntegerField(required=False)
    estadoID = serializers.IntegerField(required=False)
    fechaLimite = serializers.DateTimeField(required=False)

class eliminarEjercicioAsignadoSerializer(serializers.Serializer):
    ejercicioAsignadoID = serializers.IntegerField(required=True)