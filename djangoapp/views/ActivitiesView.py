from djangoapp.utils.api_response import response_api
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from djangoapp.services import activitiesService as service

from djangoapp.serializers.activitesSerializer import asignarEjercicioSerializer, actualizarEjercicioAsignadoSerializer, \
    eliminarEjercicioAsignadoSerializer, subirEjercicioAsignadoSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getActivities(request):
    try:
        return response_api(
            data=service.getEjerciciosAsignados(request.user.id),
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
def getActivitiesById(request, id):
    try:
        if not service.checkEjercicioAsignado(id):
            return response_api(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                error={
                    "message": f"No existe un ejercicio asignado con el ID: {id}"
                }
            )

        return response_api(
            data=service.getEjercicioAsignadoByID(id),
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asignarEjercicio(request):
    serializer = asignarEjercicioSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = service.asignarEjercicio(
                        request.user,
                        data["ejercicioID"],
                        data["pacienteID"],
                        data["fechaLimite"]
                    )

        return response_api(
            data=response,
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


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizarEjercicioAsignado(request):
    serializer = actualizarEjercicioAsignadoSerializer(data=request.data)

    try:
        # Validar los datos recibidos
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = service.actualizarEjercicioAsignado(
                        data.get("ejercicioAsignadoID"),
                        data.get("ejercicioID", None),
                        data.get("pacienteID", None),
                        data.get("estadoID", None),
                        data.get("fechaLimite", None)
                    )

        # Devolver respuesta exitosa
        return response_api(
            data=response,
            status_code=200,
            error="",
        )

    except Exception as e:
        # Manejo de excepciones y respuesta de error
        return response_api(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error={
                "message": "Error interno del servidor",
                "details": str(e)
            }
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminarEjercicioAsignado(request):
    serializer = eliminarEjercicioAsignadoSerializer(data=request.data)

    try:
        # Validar los datos recibidos
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = service.eliminarEjercicioAsignado(data.get("ejercicioAsignadoID"))

        # Devolver respuesta exitosa
        return response_api(
            data=response,
            status_code=200,
            error="",
        )

    except Exception as e:
        # Manejo de excepciones y respuesta de error
        return response_api(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error={
                "message": "Error interno del servidor",
                "details": str(e)
            }
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subirEjercicioAsignado(request):
    serializer = subirEjercicioAsignadoSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Guardar el archivo en el modelo
        response = service.subirEjercicioAsignado(request.FILES['video'], data)

        return response_api(
            data=response,
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
