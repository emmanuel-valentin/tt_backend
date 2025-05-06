from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from djangoapp.serializers.usersSeralizer import PacienteSerializer, FisioterapeutaSerializer
from djangoapp.services.user import UserService as service
from djangoapp.utils.api_response import response_api
from djangoapp.constants.role import Role


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserById(request, id):
    try:
        if not service.checkUser(id):
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={
                    "message": "No existe un usuario con ese ID"
                }
            )

        user_role = service.getUserRole(id)
        return response_api(
            data=service.getUserById(id, user_role),
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