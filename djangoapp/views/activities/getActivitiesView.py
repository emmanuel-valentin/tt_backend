from djangoapp.utils.api_response import response_api
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from djangoapp.services.activities import getActivitiesService as service

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getActivities(request):
    serializer = LoginSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        print("Hola")
    except ValidationError as e:
        return response_api(
            status="error",
            status_code=status.HTTP_400_BAD_REQUEST,
            error=e.detail,
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
        if not service.existEjercicioAsignado(id):
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={
                    "message": "No existe un ejercicio asignado con ese ID"
                }
            )

        return response_api(
            data=service.getResponse(id),
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