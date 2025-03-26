from djangoapp.models import Fisioterapeuta, Vinculacion, Feedback, EjercicioAsignado
from django.core.exceptions import ObjectDoesNotExist

def checkPhysiotherapist(id):
    return Fisioterapeuta.objects.filter(id=id).exists()

def getPhysiotherapistById(id):
    fisioterapeuta = Fisioterapeuta.objects.select_related('persona_id__user').get(id=id)

    data = {
        "id": fisioterapeuta.id,
        "cedula": fisioterapeuta.cedula,
        "codigo_token": fisioterapeuta.codigo_token,
        "persona": {
            "id": fisioterapeuta.persona_id.id,
            "fecha_nacimiento": fisioterapeuta.persona_id.fecha ,
            "nacionalidad": fisioterapeuta.persona_id.nacionalidad,
            "telefono": fisioterapeuta.persona_id.telefono,
            "foto_url": fisioterapeuta.persona_id.foto_url,
        },
        "usuario": {
            "id": fisioterapeuta.persona_id.user.id,
            "username": fisioterapeuta.persona_id.user.username,
            "first_name": fisioterapeuta.persona_id.user.first_name,
            "last_name": fisioterapeuta.persona_id.user.last_name,
            "email": fisioterapeuta.persona_id.user.email,
        }
    }
    return data

def updatePhysiotherapist(data):
    try:
        fisioterapeuta = Fisioterapeuta.objects.get(id=data["id"])

        # Actualizar los campos
        if "cedula" in data:
            fisioterapeuta.cedula = data["cedula"]
        if "codigo_token" in data:
            fisioterapeuta.codigo_token = data["codigo_token"]

        # Actualizar los datos de la persona relacionada
        if "persona" in data and data["persona"]:
            persona_data = data["persona"]
            if "fecha" in persona_data:
                fisioterapeuta.persona_id.fecha = persona_data["fecha"]
            if "nacionalidad" in persona_data:
                fisioterapeuta.persona_id.nacionalidad = persona_data["nacionalidad"]
            if "telefono" in persona_data:
                fisioterapeuta.persona_id.telefono = persona_data["telefono"]
            if "foto_url" in persona_data:
                fisioterapeuta.persona_id.foto_url = persona_data["foto_url"]
            fisioterapeuta.persona_id.save()

        # Actualizar los datos del usuario relacionado
        if "usuario" in data and data["usuario"]:
            usuario_data = data["usuario"]
            if "username" in usuario_data:
                fisioterapeuta.persona_id.user.username = usuario_data["username"]
            if "first_name" in usuario_data:
                fisioterapeuta.persona_id.user.first_name = usuario_data["first_name"]
            if "last_name" in usuario_data:
                fisioterapeuta.persona_id.user.last_name = usuario_data["last_name"]
            if "email" in usuario_data:
                fisioterapeuta.persona_id.user.email = usuario_data["email"]
            fisioterapeuta.persona_id.user.save()

        fisioterapeuta.save()
        return fisioterapeuta

    except ObjectDoesNotExist:
        return None
    except Exception as e:
        raise e

def getLinks(user_id):
    from djangoapp.services.user.PatientService import getPatientById

    vinculaciones = Vinculacion.objects.filter(paciente_id=user_id)

    if not vinculaciones.exists():
        return {"mensaje": "No hay vinculaciones para este paciente."}

    data = []
    for vinculacion in vinculaciones:
        data.append(getPatientById(vinculacion.fisioterapeuta.id))

    return {"vinculaciones": data}

def sendFeedback(data, user_id):
    try:
        ejercicio_asignado = EjercicioAsignado.objects.get(id=data["ejercicio_asignado_id"])

        fisioterapeuta = Fisioterapeuta.objects.get(persona_id__user__id=user_id)  # Obtener la instancia de Fisioterapeuta

        feedback = Feedback.objects.create(
            fisioterapeuta=fisioterapeuta,  # Pasar la instancia en lugar del ID
            ejercicio_asignado=ejercicio_asignado,  # Pasar la instancia en lugar del ID
            feedback=data.get("feedback")
        )

        return {"mensaje": "Feedback guardado exitosamente.", "feedback_id": feedback.id}

    except EjercicioAsignado.DoesNotExist:
        return {"error": "El ejercicio asignado no existe."}
    except Fisioterapeuta.DoesNotExist:
        return {"error": "El fisioterapeuta no existe."}
    except Exception as e:
        return {"error": str(e)}

