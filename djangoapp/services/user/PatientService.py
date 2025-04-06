from djangoapp.models import Paciente, Vinculacion, Fisioterapeuta

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
    try:
        fisioterapeuta = Fisioterapeuta.objects.get(codigo_token=data.get("codigo"))

        # Crear la vinculación
        link = Vinculacion(
            paciente_id=user_id,
            fisioterapeuta_id=fisioterapeuta.id,
            estado="VINCULADO"
        )
        link.save()

        return {"mensaje": "Paciente vinculado correctamente al fisioterapeuta."}

    except Fisioterapeuta.DoesNotExist:
        return {"error": "El código del fisioterapeuta no existe"}

    except Exception as e:
        return {"error": f"Ocurrió un error inesperado: {str(e)}"}

def getLinks(user_id):
    from djangoapp.services.user.PhysiotherapistService import getPhysiotherapistById

    vinculaciones = Vinculacion.objects.filter(paciente_id=user_id)

    if not vinculaciones.exists():
        return {"mensaje": "No hay vinculaciones para este paciente."}

    data = []
    for vinculacion in vinculaciones:
        data.append(getPhysiotherapistById(vinculacion.fisioterapeuta.id))

    return {"vinculaciones": data}


