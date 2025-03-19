from djangoapp.utils.api_response import response_api
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from djangoapp.services import exercisesService as service


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExercises(request):
    try:
        return response_api(
            data=service.getEjercicios(),
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
