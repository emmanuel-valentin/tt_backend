from djangoapp.models import EjercicioAsignado

def existEjercicioAsignado(id):
    return EjercicioAsignado.objects.filter(id=id).exists()

def getResponse(id):
    ejercicio_asignado = EjercicioAsignado.objects.get(id=id)
    last_name_parts = ejercicio_asignado.paciente.persona_id.user.last_name.split(" ")

    data = {
        "id": ejercicio_asignado.ejercicio.id,
        "nombre": ejercicio_asignado.ejercicio.nombre,
        "descripcion": ejercicio_asignado.ejercicio.descripcion,
        "paciente": {
            "id": ejercicio_asignado.paciente.id,
            "fotoUrl": ejercicio_asignado.paciente.persona_id.foto_url,
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
