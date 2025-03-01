from djangoapp.utils.api_response import response_api
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from djangoapp.services import activitiesService as service

class asignarEjercicioSerializer(serializers.Serializer):
    ejercicioID = serializers.IntegerField(required=True)
    pacienteID = serializers.IntegerField(required=True)
    fechaLimite = serializers.DateTimeField(required=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getActivities(request):
    try:
        return response_api(
            data=service.getEjerciciosAsignados(request.user.id),
            status_code=200,
            error="",
        )

    except Exception as e:
        return response_api(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error={
                "message": "Error interno del servidor",
                "details": str(e)
            }
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getActivitiesById(request, id):
    try:
        if not service.checkEjercicioAsignado(id):
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={
                    "message": "No existe un ejercicio asignado con ese ID"
                }
            )

        return response_api(
            data=service.getEjercicioAsignadoByID(id),
            status_code=200,
            error="",
        )

    except Exception as e:
        return response_api(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error={
                "message": "Error interno del servidor",
                "details": str(e)
            }
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asignarEjercicio(request):
    serializer = asignarEjercicioSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        access_token, refresh_token = iniciar_sesion(data)

        if access_token:
            return response_api(
                data={"message": "Login exitoso", "access_token": access_token, "refresh_token": refresh_token},
                status_code=status.HTTP_200_OK,
                error="",
            )
        else:
            return response_api(
                status="error",
                status_code=status.HTTP_401_UNAUTHORIZED,
                error={"message": "Credenciales inválidas"},
            )
    except Exception as e:
        return response_api(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error={
                "message": "Error interno del servidor",
                "details": str(e)
            }
        )