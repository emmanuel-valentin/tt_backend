from djangoapp.models import Paciente, Vinculacion, Fisioterapeuta
from djangoapp.constants.role import Role
from django.core.exceptions import ObjectDoesNotExist
from djangoapp.services.user import UserService as user_service


def checkPatient(id):
    return Paciente.objects.filter(persona_id=id).exists()


def getPatientById(id):
    paciente = Paciente.objects.select_related('persona_id__user').get(persona_id=id)

    data = {
        "id": paciente.id,
        # "ocupacion": paciente.ocupacion,
        "rol": Role.PATIENT.to_json(),
        "persona": {
            "id": paciente.persona_id.id,
            "fecha_nacimiento": paciente.persona_id.fecha,
            "telefono": paciente.persona_id.telefono,
            "foto_url": paciente.persona_id.foto_url,
        },
        "usuario": {
            "id": paciente.persona_id.user.id,
            "username": paciente.persona_id.user.username,
            "first_name": paciente.persona_id.user.first_name,
            "last_name": paciente.persona_id.user.last_name,
            "email": paciente.persona_id.user.email,
        }
    }
    return data


def updatePatient(data):
    try:
        paciente = Paciente.objects.get(id=data["id"])

        # Actualizar los campos
        if "ocupacion" in data:
            paciente.ocupacion = data["ocupacion"]

        # Actualizar los datos de la persona relacionada
        if "persona" in data and data["persona"]:
            persona_data = data["persona"]
            if "fecha" in persona_data:
                paciente.persona_id.fecha = persona_data["fecha"]
            if "telefono" in persona_data:
                paciente.persona_id.telefono = persona_data["telefono"]
            if "foto_url" in persona_data:
                paciente.persona_id.foto_url = persona_data["foto_url"]
            paciente.persona_id.save()

        # Actualizar los datos del usuario relacionado
        if "usuario" in data and data["usuario"]:
            usuario_data = data["usuario"]
            if "username" in usuario_data:
                paciente.persona_id.user.username = usuario_data["username"]
            if "first_name" in usuario_data:
                paciente.persona_id.user.first_name = usuario_data["first_name"]
            if "last_name" in usuario_data:
                paciente.persona_id.user.last_name = usuario_data["last_name"]
            if "email" in usuario_data:
                paciente.persona_id.user.email = usuario_data["email"]
            paciente.persona_id.user.save()

        paciente.save()
        return paciente

    except ObjectDoesNotExist:
        return None
    except Exception as e:
        raise e


def linkPatientToPhysiotherapist(user_id, data):
    persona_id = user_service.getPersonaIdByUserId(user_id)
    paciente_id = getPatientById(persona_id)["id"]
    fisioterapeuta = Fisioterapeuta.objects.get(codigo_token=data.get("codigo"))

    # Crear la vinculación
    link = Vinculacion(
        paciente_id=paciente_id,
        fisioterapeuta_id=fisioterapeuta.id,
        estado="PENDIENTE"
    )
    link.save()

    return {"mensaje": "Solicitud de vinculacuón enviada correctamente."}


def getLinks(user_id):
    from djangoapp.services.user.PhysiotherapistService import getPhysiotherapistById

    try:
        # Obtener el paciente usando el user_id
        paciente = Paciente.objects.get(persona_id__user__id=user_id)

        # Obtener todas las vinculaciones del paciente
        vinculaciones = Vinculacion.objects.filter(paciente=paciente)

        # if not vinculaciones.exists():
        #     return {"mensaje": "No hay vinculaciones para este paciente."}

        data = []
        for vinculacion in vinculaciones:
            if vinculacion.fisioterapeuta:
                fisio_data = getPhysiotherapistById(vinculacion.fisioterapeuta.persona_id.id)
                # Añadir información de vinculación
                fisio_data["vinculacion_id"] = vinculacion.id
                fisio_data["vinculacion_estado"] = vinculacion.estado
                data.append(fisio_data)

        return data

    except Paciente.DoesNotExist:
        return {"error": "El paciente no existe."}
    except Exception as e:
        raise e


def desvincularVinculacion(paciente_id, vinculacion_id):
    vinculacion = Vinculacion.objects.get(id=vinculacion_id, paciente_id=paciente_id)
    vinculacion.estado = "DESVINCULADO"
    vinculacion.save()
    return {"mensaje": "Vinculación desvinculada exitosamente."}
