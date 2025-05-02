from djangoapp.models import Paciente, Fisioterapeuta, Persona
from djangoapp.constants.role import Role
from djangoapp.services.user import PatientService, PhysiotherapistService


def checkUser(id):
    return PatientService.checkPatient(id) or PhysiotherapistService.checkPhysiotherapist(id)


def getUserRole(id):
    if PatientService.checkPatient(id):
        return Role.PATIENT
    elif PhysiotherapistService.checkPhysiotherapist(id):
        return Role.PHYSIOTHERAPIST
    else:
        raise ValueError(f"Cannot resolve role for user with id {id}")


def getUserById(id, role):
    if role == Role.PATIENT:
        return PatientService.getPatientById(id)
    elif role == Role.PHYSIOTHERAPIST:
        return PhysiotherapistService.getPhysiotherapistById(id)
    else:
        raise ValueError("Invalid role")


def updateUser(data, role):
    if role == Role.PATIENT:
        return PatientService.updatePatient(data)
    elif role == Role.PHYSIOTHERAPIST:
        return PhysiotherapistService.updatePhysiotherapist(data)
    else:
        raise ValueError("Invalid role")


def getPersonaIdByUserId(user_id):
    try:
        # Consulta directamente al modelo Persona
        persona = Persona.objects.get(user_id=user_id)
        return persona.id
    except Persona.DoesNotExist:
        raise ValueError(f"No se encontró una Persona asociada al usuario con id {user_id}")
    except Exception as e:
        raise ValueError(f"Error al buscar la persona: {str(e)}")
