from djangoapp.models import Paciente

def checkPatient(id):
    return Paciente.objects.filter(id=id).exists()

def getPatientById(id):
    paciente = Paciente.objects.select_related('persona_id__user').get(id=id)

    data = {
        "id": paciente.id,
        "ocupacion": paciente.ocupacion,
        "persona": {
            "id": paciente.persona_id.id,
            "fecha_nacimiento": paciente.persona_id.fecha ,
            "nacionalidad": paciente.persona_id.nacionalidad,
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
            if "nacionalidad" in persona_data:
                paciente.persona_id.nacionalidad = persona_data["nacionalidad"]
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