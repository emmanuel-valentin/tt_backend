from djangoapp.models import Persona
from django.core.exceptions import ObjectDoesNotExist
import os

def subirFoto(user, foto_file):
    try:
        persona = Persona.objects.get(user=user)
        persona.foto_url = foto_file
        persona.save()
        return {
            "message": "Foto subida exitosamente.",
            "foto_url": persona.foto_url.url if persona.foto_url else None
        }
    except ObjectDoesNotExist:
        raise Exception("No se encontró una Persona asociada al usuario.")

def deletePhotoProfile(user):
    try:
        persona = Persona.objects.get(user=user)

        if persona.foto_url:
            file_path = persona.foto_url.path
            persona.foto_url.delete(save=False)

            if os.path.isfile(file_path):
                os.remove(file_path)

        persona.foto_url = None
        persona.save()

        return {
            "message": "Foto eliminada exitosamente.",
            "foto_url": None
        }

    except ObjectDoesNotExist:
        raise Exception("No se encontró una Persona asociada al usuario.")
