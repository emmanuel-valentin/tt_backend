from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status

from djangoapp.serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        response = Response({"user": UserSerializer(user).data}, status=status.HTTP_200_OK)

        response.set_cookie(
            key='token',
            value=token.key,
        )

        return response

    return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)

        response = Response({"user": serializer.data}, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key='token',
            value=token.key,
        )

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def test(request):
    return Response({"message": "Acceso permitido, estás autenticado!"})
