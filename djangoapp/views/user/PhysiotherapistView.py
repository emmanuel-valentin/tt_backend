from djangoapp.utils.api_response import response_api
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from djangoapp.services.user import PhysiotherapistService as service
from djangoapp.serializers.usersSeralizer import FisioterapeutaSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPhysiotherapistById(request, id):
    try:
        if not service.checkPhysiotherapist(id):
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={
                    "message": "No existe un ejercicio asignado con ese ID"
                }
            )

        return response_api(
            data=service.getPhysiotherapistById(id),
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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePhysiotherapist(request):
    try:
        if not service.checkPhysiotherapist(request.data["id"]):
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={"message": "No existe un fisioterapeuta con ese ID"}
            )

        # Use the serializer to validate the data
        serializer = FisioterapeutaSerializer(data=request.data)
        if not serializer.is_valid():
            return response_api(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                error={"message": "Datos inválidos", "details": serializer.errors}
            )

        fisioterapeuta_actualizado = service.updatePhysiotherapist(serializer.validated_data)

        if fisioterapeuta_actualizado is None:
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={"message": "No se pudo actualizar el fisioterapeuta"}
            )

        return response_api(
            data=service.getPhysiotherapistById(request.data["id"]),
            status_code=status.HTTP_200_OK,
            error="",
        )

    except Exception as e:
        return response_api(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error={"message": "Error interno del servidor", "details": str(e)}
        )