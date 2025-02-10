from djangoapp.utils.api_response import response_api
from rest_framework import status

def validate_serializer(serializer):
    """
    Valida el serializer y retorna una respuesta de error si no es válido.
    """
    if not serializer.is_valid():
        return response_api(
            status="error",
            status_code=status.HTTP_400_BAD_REQUEST,
            error={
                "message": "Faltan campos requeridos",
                "details": serializer.errors
            }
        )
    return serializer.validated_data
