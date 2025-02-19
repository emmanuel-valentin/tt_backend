from rest_framework.exceptions import ValidationError

def validate_serializer(serializer):
    """
    Valida el serializer y lanza una excepción si no es válido.
    """
    if not serializer.is_valid():
        raise ValidationError({
            "message": "Ocurrio un error en algun campo",
            "details": serializer.errors
        })
    return serializer.validated_data
