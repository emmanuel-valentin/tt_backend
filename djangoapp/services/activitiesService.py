from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from djangoapp.models import Ejercicio, EjercicioAsignado, Vinculacion, Paciente, Estado, Fisioterapeuta, SeguimientoIA


def checkEjercicioAsignado(id):
    return EjercicioAsignado.objects.filter(id=id).exists()

def getEjercicioAsignadoByID(id):
    ejercicio_asignado = EjercicioAsignado.objects.get(id=id)
    last_name_parts = ejercicio_asignado.paciente.persona_id.user.last_name.split(" ")

    data = {
        "id": ejercicio_asignado.ejercicio.id,
        "nombre": ejercicio_asignado.ejercicio.nombre,
        "descripcion": ejercicio_asignado.ejercicio.descripcion,
        "urlVideo": ejercicio_asignado.ejercicio.url_video,
        "paciente": {
            "id": ejercicio_asignado.paciente.id,
            "fotoUrl": ejercicio_asignado.paciente.persona_id.foto_url,
            "urlVideoPaciente": (SeguimientoIA.objects.filter(paciente=ejercicio_asignado.paciente.id).first()).url_video_paciente,
            "nombre": ejercicio_asignado.paciente.persona_id.user.first_name,
            "apellidoPat": last_name_parts[0] if last_name_parts else ""
        }
    }

    # Solo agregar "apellidoMat" si hay un segundo apellido
    if len(last_name_parts) > 1:
        data["paciente"]["apellidoMat"] = last_name_parts[1]
    else:
        data["paciente"]["apellidoMat"] = ""

    return data

def getEjerciciosAsignados(user_id):
    ejercicios_asignados = EjercicioAsignado.objects.filter(paciente__persona_id__user__id=user_id)

    resultado = []
    for ejercicio_asignado in ejercicios_asignados:
        last_name_parts = ejercicio_asignado.paciente.persona_id.user.last_name.split(" ")

        # Obtener la vinculación del fisioterapeuta con el paciente
        vinculacion = Vinculacion.objects.filter(paciente=ejercicio_asignado.paciente).first()

        # Si hay un fisioterapeuta vinculado, obtener sus datos
        fisioterapeuta_data = {}
        if vinculacion and vinculacion.fisioterapeuta:
            fisioterapeuta = vinculacion.fisioterapeuta
            persona_fisio = fisioterapeuta.persona_id

            fisioterapeuta_data = {
                "id": fisioterapeuta.id,
                "fotoUrl": persona_fisio.foto_url,
                "nombre": persona_fisio.user.first_name,
                "apellidoPat": persona_fisio.user.last_name.split(" ")[0] if persona_fisio.user.last_name else "",
                "apellidoMat": persona_fisio.user.last_name.split(" ")[1] if len(persona_fisio.user.last_name.split(" ")) > 1 else ""
            }

        seguimiento = SeguimientoIA.objects.filter(paciente=ejercicio_asignado.paciente).first()
        data = {
            "id": ejercicio_asignado.ejercicio.id,
            "nombre": ejercicio_asignado.ejercicio.nombre,
            "descripcion": ejercicio_asignado.ejercicio.descripcion,
            "fechaAsignada": ejercicio_asignado.fecha_asignada,
            "fechaLimite": ejercicio_asignado.fecha_limite,
            "estado": ejercicio_asignado.estado.estado,
            "urlVideo": ejercicio_asignado.ejercicio.url_video,
            "paciente": {
                "id": ejercicio_asignado.paciente.id,
                "fotoUrl": ejercicio_asignado.paciente.persona_id.foto_url,
                "urlVideoPaciente": seguimiento.url_video_paciente if seguimiento else None,
                "nombre": ejercicio_asignado.paciente.persona_id.user.first_name,
                "apellidoPat": last_name_parts[0] if last_name_parts else "",
                "apellidoMat": last_name_parts[1] if len(last_name_parts) > 1 else ""

            },
            "fisioterapeuta": fisioterapeuta_data
        }
        resultado.append(data)

    return resultado

def asignarEjercicio(user, ejercicioID, pacienteID, fechaLimite):
    # Verificar que el usuario esté asociado a un fisioterapeuta
    if not Fisioterapeuta.objects.filter(persona_id__user=user).exists():
        raise PermissionDenied("El usuario no tiene permisos para asignar ejercicios.")

    # Verificar si el ejercicio existe
    try:
        ejercicio = Ejercicio.objects.get(id=ejercicioID)
    except Ejercicio.DoesNotExist:
        raise ValueError("El ejercicio especificado no existe.")

    # Verificar si el paciente existe
    try:
        paciente = Paciente.objects.get(id=pacienteID)
    except Paciente.DoesNotExist:
        raise ValueError("El paciente especificado no existe.")

    # Obtener el fisioterapeuta asignado al paciente
    vinculacion = Vinculacion.objects.filter(paciente=paciente).first()
    fisioterapeuta = vinculacion.fisioterapeuta if vinculacion else None

    # Crear la asignación del ejercicio
    ejercicio_asignado = EjercicioAsignado.objects.create(
        ejercicio=ejercicio,
        paciente=paciente,
        fecha_asignada=timezone.now(),
        fecha_limite=fechaLimite,
        estado=Estado.objects.get(estado="ASIGNADO") 
    )

    return {
        "id": ejercicio_asignado.id,
        "nombre": ejercicio.nombre,
        "descripcion": ejercicio.descripcion,
        "fechaAsignada": ejercicio_asignado.fecha_asignada,
        "fechaLimite": ejercicio_asignado.fecha_limite,
        "estado": ejercicio_asignado.estado.estado,
        "paciente": {
            "id": paciente.id,
            "nombre": paciente.persona_id.user.first_name,
            "apellidoPat": paciente.persona_id.user.last_name.split(" ")[0] if paciente.persona_id.user.last_name else "",
            "apellidoMat": paciente.persona_id.user.last_name.split(" ")[1] if len(paciente.persona_id.user.last_name.split(" ")) > 1 else "",
            "fotoUrl": paciente.persona_id.foto_url
        },
        "fisioterapeuta": {
            "id": fisioterapeuta.id if fisioterapeuta else "",
            "nombre": fisioterapeuta.persona_id.user.first_name if fisioterapeuta else "",
            "apellidoPat": fisioterapeuta.persona_id.user.last_name.split(" ")[0] if fisioterapeuta and fisioterapeuta.persona_id.user.last_name else "",
            "apellidoMat": fisioterapeuta.persona_id.user.last_name.split(" ")[1] if fisioterapeuta and len(fisioterapeuta.persona_id.user.last_name.split(" ")) > 1 else "",
            "fotoUrl": fisioterapeuta.persona_id.foto_url if fisioterapeuta else ""
        }
    }

def actualizarEjercicioAsignado(ejercicioAsignadoID, ejercicioID, pacienteID, nuevo_estado, nueva_fecha_limite):
    try:
        # Intentamos obtener el EjercicioAsignado a través del ID
        ejercicio_asignado = EjercicioAsignado.objects.get(id=ejercicioAsignadoID)

        # Actualizamos los campos opcionales si se proporcionan
        if ejercicioID:
            ejercicio = Ejercicio.objects.get(id=ejercicioID)
            ejercicio_asignado.ejercicio = ejercicio

        if pacienteID:
            paciente = Paciente.objects.get(id=pacienteID)
            ejercicio_asignado.paciente = paciente

        if nuevo_estado:
            estado = Estado.objects.get(id=nuevo_estado)
            ejercicio_asignado.estado = estado

        if nueva_fecha_limite:
            ejercicio_asignado.fecha_limite = nueva_fecha_limite

        ejercicio_asignado.save()

        return {
            "id": ejercicio_asignado.id,
            "nombre": ejercicio_asignado.ejercicio.nombre,
            "descripcion": ejercicio_asignado.ejercicio.descripcion,
            "fechaAsignada": ejercicio_asignado.fecha_asignada,
            "fechaLimite": ejercicio_asignado.fecha_limite,
            "estado": ejercicio_asignado.estado.estado,
            "paciente": {
                "id": ejercicio_asignado.paciente.id,
                "nombre": ejercicio_asignado.paciente.persona_id.user.first_name,
                "apellidoPat": ejercicio_asignado.paciente.persona_id.user.last_name.split(" ")[
                    0] if ejercicio_asignado.paciente.persona_id.user.last_name else "",
                "apellidoMat": ejercicio_asignado.paciente.persona_id.user.last_name.split(" ")[1] if len(
                    ejercicio_asignado.paciente.persona_id.user.last_name.split(" ")) > 1 else "",
                "fotoUrl": ejercicio_asignado.paciente.persona_id.foto_url
            },
            "ejercicio": {
                "id": ejercicio_asignado.ejercicio.id,
                "nombre": ejercicio_asignado.ejercicio.nombre,
                "descripcion": ejercicio_asignado.ejercicio.descripcion,
                "urlVideo": ejercicio_asignado.ejercicio.url_video
            }
        }

    except EjercicioAsignado.DoesNotExist:
        raise ValueError("El ejercicio asignado especificado no existe.")
    except Ejercicio.DoesNotExist:
        raise ValueError("El ejercicio especificado no existe.")
    except Paciente.DoesNotExist:
        raise ValueError("El paciente especificado no existe.")
    except Estado.DoesNotExist:
        raise ValueError("El estado especificado no existe.")

def eliminarEjercicioAsignado(ejercicioID):
    # Verificar si el ejercicio asignado existe
    try:
        ejercicio_asignado = EjercicioAsignado.objects.get(id=ejercicioID)
    except EjercicioAsignado.DoesNotExist:
        raise ValueError("El ejercicio asignado no existe.")

    # Eliminar el ejercicio asignado
    ejercicio_asignado.delete()

    return {"mensaje": "Ejercicio asignado eliminado con éxito"}
