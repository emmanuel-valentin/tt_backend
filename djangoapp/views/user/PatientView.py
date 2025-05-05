from djangoapp.utils.api_response import response_api
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from djangoapp.services.user import PatientService as service
from djangoapp.serializers.usersSeralizer import LinkPatientToPhysiotherapistSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPatientById(request, id):
    try:
        if not service.checkPatient(id):
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={
                    "message": "No existe un ejercicio asignado con ese ID"
                }
            )

        return response_api(
            data=service.getPatientById(id),
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLinks(request):
    try:
        return response_api(
            data=service.getLinks(request.user.id),
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
def updatePatient(request):
    try:
        if not service.checkPatient(request.data["id"]):
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={"message": "No existe un Paciente con ese ID"}
            )

        # Use the serializer to validate the data
        serializer = PacienteSerializer(data=request.data)
        if not serializer.is_valid():
            return response_api(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                error={"message": "Datos inválidos", "details": serializer.errors}
            )

        paciente_actualizado = service.updatePatient(serializer.validated_data)

        if paciente_actualizado is None:
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={"message": "No se pudo actualizar el Paciente"}
            )

        return response_api(
            data=service.getPatientById(request.data["id"]),
            status_code=status.HTTP_200_OK,
            error="",
        )

    except Exception as e:
        return response_api(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error={"message": "Error interno del servidor", "details": str(e)}
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def linkPatientToPhysiotherapist(request):
    serializer = LinkPatientToPhysiotherapistSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = service.linkPatientToPhysiotherapist(request.user.id, data)

        return response_api(
            status="success",
            data=response,
            status_code=status.HTTP_200_OK,
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