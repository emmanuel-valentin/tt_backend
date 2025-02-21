from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from djangoapp.utils.api_response import response_api
from djangoapp.views.auth.loginView import login


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test(request):
    try:
        # Verifica si el token es válido
        user = request.user  # Esto solo se obtiene si el token es válido
        print(user)
        return Response({"message": "Acceso permitido, usuario autenticado"})

    except AuthenticationFailed as e:
        # Si el token expiró, intentamos renovarlo usando el refresh_token
        refresh_token = request.COOKIES.get('refresh_token')  # O recibirlo desde el frontend
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)

                return response_api(
                    data={"message": "Token renovado", "access_token": new_access_token},
                    status_code=200,
                    error="",
                )
            except Exception as e:
                return response_api(
                    status="error",
                    status_code=401,
                    error={"message": "Refresh token inválido, inicia sesión nuevamente"},
                )

        return response_api(
            status="error",
            status_code=401,
            error={"message": "Token de acceso expirado, por favor inicia sesión"},
        )
