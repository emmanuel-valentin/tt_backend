from djangoapp.models import Ejercicio


def getEjercicios():
    ejercicios = Ejercicio.objects.all()

    resultado = []

    for ejercicio in ejercicios:
        data = {
            "nombre": ejercicio.nombre,
            "tipo": ejercicio.tipo,
            "descripcion": ejercicio.descripcion,
            "url_video": ejercicio.url_video
        }
        resultado.append(data)

    return resultado