from djangoapp.models import Fisioterapeuta

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