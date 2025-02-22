import os
import sys
import django
import random
import string

from faker import Faker
from django.utils import timezone
from datetime import timedelta

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tt_backend.settings")
django.setup()

fake = Faker()

from django.contrib.auth.models import User
from djangoapp.models import Estado, Persona, Paciente, Fisioterapeuta, Ejercicio, EjercicioAsignado


# Función para generar el código token único
def generar_codigo_token():
    while True:
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Fisioterapeuta.objects.filter(codigo_token=codigo).exists():
            return codigo


# Crear estados solo si no existen
estados = ["ASIGNADO", "FINALIZADO", "NO REALIZADO", "ATRASADO", "CANCELADO"]
for estado in estados:
    if not Estado.objects.filter(estado=estado).exists():
        Estado.objects.create(estado=estado)
        print(f"Estado '{estado}' creado")
    else:
        print(f"Estado '{estado}' ya existe")

print("Estados generados exitosamente")

# Crear usuarios aleatorios con nombres y apellidos
NUM_USUARIOS = 30
personas = []

for _ in range(NUM_USUARIOS):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = "123"

    if not User.objects.filter(username=email).exists():
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        print(f"Usuario '{email}' ({first_name} {last_name}) creado")

        # Crear la Persona asociada a este usuario
        persona = Persona.objects.create(
            user=user,
            fecha=fake.date_this_century(),
            nacionalidad=fake.country(),
            telefono=fake.phone_number(),
            foto_url=fake.image_url()
        )
        personas.append(persona)  # Guardamos la persona creada en una lista
        print(f"Persona asociada al usuario '{email}' creada")
    else:
        print(f"Usuario '{email}' ya existía, saltando...")

print("Usuarios y personas generados exitosamente")

# Asignar 5 pacientes y 5 fisioterapeutas
pacientes = []
fisioterapeutas = []

for i, persona in enumerate(personas):
    if i < len(personas) / 2:
        # Crear pacientes
        paciente = Paciente.objects.create(
            persona_id=persona,
            ocupacion=fake.job()  # Asignamos una ocupación aleatoria al paciente
        )
        pacientes.append(paciente)
        print(f"Paciente {persona.user.username} creado")
    else:
        # Crear fisioterapeutas
        fisioterapeuta = Fisioterapeuta.objects.create(
            persona_id=persona,
            cedula=fake.ssn(),  # Generamos una cédula aleatoria
            codigo_token=generar_codigo_token()  # Generamos un código token único
        )
        fisioterapeutas.append(fisioterapeuta)
        print(f"Fisioterapeuta {persona.user.username} creado")

print("Pacientes y fisioterapeutas asignados exitosamente")

# Crear algunos ejercicios si no existen
ejercicios = [
    {"nombre": "Ejercicio 1", "descripcion": fake.text(), "tipo": "Rehabilitación", "url_video": fake.url()},
    {"nombre": "Ejercicio 2", "descripcion": fake.text(), "tipo": "Rehabilitación", "url_video": fake.url()},
    {"nombre": "Ejercicio 3", "descripcion": fake.text(), "tipo": "Fortalecimiento", "url_video": fake.url()},
    {"nombre": "Ejercicio 4", "descripcion": fake.text(), "tipo": "Fortalecimiento", "url_video": fake.url()},
    {"nombre": "Ejercicio 5", "descripcion": fake.text(), "tipo": "Estiramiento", "url_video": fake.url()},
]

for ejercicio_data in ejercicios:
    if not Ejercicio.objects.filter(nombre=ejercicio_data["nombre"]).exists():
        ejercicio = Ejercicio.objects.create(**ejercicio_data)
        print(f"Ejercicio '{ejercicio.nombre}' creado")
    else:
        print(f"Ejercicio '{ejercicio_data['nombre']}' ya existe")

# Asignar ejercicios a los pacientes
for paciente in pacientes:
    # Seleccionar 2 ejercicios aleatorios para cada paciente
    ejercicios_asignados = random.sample(list(Ejercicio.objects.all()), 2)

    for ejercicio in ejercicios_asignados:
        # Verificar si la asignación de este ejercicio al paciente ya existe
        if not EjercicioAsignado.objects.filter(paciente=paciente, ejercicio=ejercicio).exists():
            estado = random.choice(Estado.objects.all())

            fecha_asignada = timezone.now()
            fecha_limite = timezone.now() + timedelta(days=7)

            # Crear la relación EjercicioAsignado
            EjercicioAsignado.objects.create(
                paciente=paciente,
                ejercicio=ejercicio,
                estado=estado,
                fecha_asignada=fecha_asignada,
                fecha_limite=fecha_limite
            )
            print(f"Ejercicio '{ejercicio.nombre}' asignado al paciente {paciente.persona_id.user.username}")
        else:
            print(f"El ejercicio '{ejercicio.nombre}' ya ha sido asignado al paciente {paciente.persona_id.user.username}")

print("Ejercicios asignados a los pacientes exitosamente")
