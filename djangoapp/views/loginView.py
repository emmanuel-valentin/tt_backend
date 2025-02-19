from djangoapp.services.loginService import iniciar_sesion
from djangoapp.utils.api_response import response_api
from rest_framework import status, serializers
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from djangoapp.utils.validations import validate_serializer


class LogingSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    serializer = LogingSerializer(data=request.data)

    try:
        data = validate_serializer(serializer)
        access_token = iniciar_sesion(data)

        if access_token:
            return response_api(
                data={"message": "Login exitoso", "token": access_token},
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
                "message": "Error al crear el usuario, persona, paciente o relacionar el expediente",
                "details": str(e)
            }
        )
