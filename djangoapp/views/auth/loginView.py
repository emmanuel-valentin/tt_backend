from djangoapp.services.auth.loginService import iniciar_sesion
from djangoapp.utils.api_response import response_api
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from djangoapp.serializers.authSerializer import LoginSerializer

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)

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