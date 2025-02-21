from djangoapp.utils.api_response import response_api
from rest_framework import status, serializers
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError  # Importamos IntegrityError
from djangoapp.services.registerService import crear_usuario
from djangoapp.utils.validations import validate_serializer


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


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    try:
        data = validate_serializer(serializer)
        crear_usuario(data)
        return response_api(
            data={"message": "Usuario Creado Correctamente"},
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
