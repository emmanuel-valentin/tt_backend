from djangoapp.models import Fisioterapeuta, Vinculacion, Feedback, EjercicioAsignado
from djangoapp.constants.role import Role
from django.core.exceptions import ObjectDoesNotExist


def checkPhysiotherapist(id):
    return Fisioterapeuta.objects.filter(persona_id=id).exists()

def getPhysiotherapistById(id):
    fisioterapeuta = Fisioterapeuta.objects.select_related('persona_id__user').get(persona_id=id)

    data = {
        "id": fisioterapeuta.id,
        "cedula": fisioterapeuta.cedula,
        "codigo_token": fisioterapeuta.codigo_token,
        "rol": Role.PHYSIOTHERAPIST.to_json(),
        "persona": {
            "id": fisioterapeuta.persona_id.id,
            "fecha": fisioterapeuta.persona_id.fecha,
            "telefono": fisioterapeuta.persona_id.telefono,
            "foto_url": str(fisioterapeuta.persona_id.foto_url),
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
            if "telefono" in persona_data:
                fisioterapeuta.persona_id.telefono = persona_data["telefono"]
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


def getLinks(user_id, estado=None):
    from djangoapp.services.user.PatientService import getPatientById

    try:
        # Obtener el fisioterapeuta usando el user_id
        fisioterapeuta = Fisioterapeuta.objects.get(persona_id__user__id=user_id)
        
        # Filtrar vinculaciones según el estado (si se proporciona)
        if estado:
            vinculaciones = Vinculacion.objects.filter(
                fisioterapeuta=fisioterapeuta,
                estado=estado
            )
        else:
            vinculaciones = Vinculacion.objects.filter(fisioterapeuta=fisioterapeuta)

        if not vinculaciones.exists():
            # mensaje = "No hay vinculaciones"
            # if estado:
            #     mensaje += f" con estado '{estado}'"
            # mensaje += " para este fisioterapeuta."
            return []

        data = []
        for vinculacion in vinculaciones:
            if vinculacion.paciente and vinculacion.paciente.persona_id:
                paciente_data = getPatientById(vinculacion.paciente.persona_id.id)
                # The profile photo is already handled in getPatientById as str(paciente.persona_id.foto_url)
                # Añadir información de vinculación
                paciente_data["vinculacion_id"] = vinculacion.id
                paciente_data["vinculacion_estado"] = vinculacion.estado
                data.append(paciente_data)

        return data
        
    except Fisioterapeuta.DoesNotExist:
        return {"error": "El fisioterapeuta no existe."}
    except Exception as e:
        raise e


def sendFeedback(data, user_id):
    try:
        ejercicio_asignado = EjercicioAsignado.objects.get(id=data["ejercicio_asignado_id"])
        fisioterapeuta = Fisioterapeuta.objects.get(persona_id__user__id=user_id)

        feedback = Feedback.objects.create(
            fisioterapeuta=fisioterapeuta,
            ejercicio_asignado=ejercicio_asignado,
            feedback=str(data.get("feedback")),
            feedback_audio=data.get("audio"),
            feedback_imagen=data.get("video")
        )

        return {"mensaje": "Feedback guardado exitosamente.", "feedback_id": feedback.id}

    except EjercicioAsignado.DoesNotExist:
        return {"error": "El ejercicio asignado no existe."}
    except Fisioterapeuta.DoesNotExist:
        return {"error": "El fisioterapeuta no existe."}
    except Exception as e:
        return {"error": str(e)}


def acceptLink(vinculacion_id, user_id):
    try:
        # Verificar si el usuario es un fisioterapeuta
        fisioterapeuta = Fisioterapeuta.objects.get(persona_id__user__id=user_id)
        
        # Buscar la vinculación
        vinculacion = Vinculacion.objects.get(id=vinculacion_id, fisioterapeuta=fisioterapeuta)
        
        # Actualizar el estado de la vinculación
        vinculacion.estado = "VINCULADO"
        vinculacion.save()
        
        return {"mensaje": "Vinculación aceptada exitosamente."}
    
    except Fisioterapeuta.DoesNotExist:
        raise Fisioterapeuta.DoesNotExist("El fisioterapeuta no existe.")
    except Vinculacion.DoesNotExist:
        raise Vinculacion.DoesNotExist("La vinculación no existe o no pertenece a este fisioterapeuta.")
    except Exception as e:
        raise e


def rejectLink(vinculacion_id, user_id):
    try:
        # Verificar si el usuario es un fisioterapeuta
        fisioterapeuta = Fisioterapeuta.objects.get(persona_id__user__id=user_id)
        
        # Buscar la vinculación
        vinculacion = Vinculacion.objects.get(id=vinculacion_id, fisioterapeuta=fisioterapeuta)
        
        # Eliminar completamente el registro de vinculación
        vinculacion.delete()
        return {"mensaje": "Vinculación rechazada y eliminada exitosamente."}
    
    except Fisioterapeuta.DoesNotExist:
        raise Fisioterapeuta.DoesNotExist("El fisioterapeuta no existe.")
    except Vinculacion.DoesNotExist:
        raise Vinculacion.DoesNotExist("La vinculación no existe o no pertenece a este fisioterapeuta.")
    except Exception as e:
        raise e
