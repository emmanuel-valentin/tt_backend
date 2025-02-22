import os
import sys
import django

# Configurar Django
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tt_backend.settings")
django.setup()

# Importar los modelos
from django.contrib.auth.models import User
from djangoapp.models import Estado, Persona, Paciente, Fisioterapeuta, Ejercicio, EjercicioAsignado

# Borrar los datos de los modelos de forma segura, respetando las dependencias
def borrar_datos():
    # Borrar EjercicioAsignado primero (tiene relaciones de claves foráneas)
    EjercicioAsignado.objects.all().delete()
    print("Datos de EjercicioAsignado borrados")

    # Borrar Paciente y Fisioterapeuta
    Paciente.objects.all().delete()
    Fisioterapeuta.objects.all().delete()
    print("Datos de Paciente y Fisioterapeuta borrados")

    # Borrar Ejercicio
    Ejercicio.objects.all().delete()
    print("Datos de Ejercicio borrados")

    # Borrar Persona (primero eliminamos las relaciones con User)
    Persona.objects.all().delete()
    print("Datos de Persona borrados")

    # Borrar User
    User.objects.all().delete()
    print("Datos de User borrados")

    # Borrar Estados
    Estado.objects.all().delete()
    print("Datos de Estado borrados")

# Ejecutar la función para borrar los datos
if __name__ == "__main__":
    borrar_datos()
    print("Todos los datos de los modelos han sido borrados exitosamente.")
