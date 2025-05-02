from djangoapp.utils.api_response import response_api
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from djangoapp.services.auth.registerService import crear_usuario
from djangoapp.utils.validations import validate_serializer

from djangoapp.serializers.authSerializer import RegisterSerializer

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    try:
        data = validate_serializer(serializer)
        access_token, refresh_token = crear_usuario(data)
        
        return response_api(
            data={
                "message": "Usuario Creado Correctamente",
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status_code=status.HTTP_201_CREATED
        )

    except ValidationError as e:
        return response_api(
            status="error",
            status_code=status.HTTP_400_BAD_REQUEST,
            error=e.detail
        )

    except IntegrityError as e:
        if 'duplicate key value violates unique constraint' in str(e):
            return response_api(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                error={
                    "message": "El correo electrónico ya está registrado.",
                }
            )

        return response_api(
            status="error",
            status_code=status.HTTP_400_BAD_REQUEST,
            error={
                "message": "Error de integridad en la base de datos.",
                "details": str(e)
            }
        )

    except Exception as e:
        return response_api(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error={
                "message": "Error al crear el usuario",
                "details": str(e)
            }
        )
