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