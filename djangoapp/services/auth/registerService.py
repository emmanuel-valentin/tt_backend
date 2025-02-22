import random
import string
from djangoapp.models import Fisioterapeuta, Persona, Paciente
from django.contrib.auth.models import User

def generar_codigo_token():
    while True:
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Fisioterapeuta.objects.filter(codigo_token=codigo).exists():
            return codigo

def crear_usuario(data):
    user = User.objects.create_user(
        username=data['email'],
        email=data['email'],
        password=data['password'],
        first_name=data['nombre'],
        last_name=f"{data['apellidoPaterno']} {data['apellidoMaterno']}",  # Apellidos concatenados
    )

    persona = Persona.objects.create(
        fecha=data['fechaNacimiento'],
        nacionalidad=data['nacionalidad'],
        telefono=data['telefono'],
        foto_url=None,
        user=user
    )

    if data.get('cedula'):
        codigo_token = generar_codigo_token()
        Fisioterapeuta.objects.create(
            persona_id=persona,
            cedula=data['cedula'],
            codigo_token=codigo_token
        )
    else:
        Paciente.objects.create(
            persona_id=persona,
            ocupacion=None
        )

    return user, persona
