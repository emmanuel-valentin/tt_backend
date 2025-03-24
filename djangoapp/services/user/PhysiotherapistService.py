from djangoapp.models import Fisioterapeuta
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