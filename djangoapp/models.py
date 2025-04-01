from django.db import models
from django.contrib.auth.models import User

class Expediente(models.Model):
    titulo = models.CharField(max_length=45, null=True)
    descripcion = models.TextField(null=True)
    fecha = models.DateTimeField(null=True)

    class Meta:
        db_table = 'Expediente'

class Persona(models.Model):
    fecha = models.DateField(null=True)
    nacionalidad = models.CharField(max_length=100, null=True)
    telefono = models.CharField(max_length=45, null=True)
    foto_url = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Persona'

class Paciente(models.Model):
    persona_id = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True)
    ocupacion = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'Paciente'

class Fisioterapeuta(models.Model):
    persona_id = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True)
    cedula = models.CharField(max_length=100, null=True)
    codigo_token = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'Fisioterapeuta'

class ExpedienteHasPaciente(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_asociacion = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Expediente_Has_Paciente'
        unique_together = ('expediente', 'paciente')


class Estado(models.Model):
    estado = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'Estado'

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=45, null=True)
    tipo = models.CharField(max_length=45, null=True)
    descripcion = models.TextField(null=True)
    url_video = models.URLField(max_length=200, null=True)

    class Meta:
        db_table = 'Ejercicio'

class Vinculacion(models.Model):
    fisioterapeuta = models.ForeignKey(Fisioterapeuta, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'Vinculacion'
        unique_together = ('fisioterapeuta', 'paciente')

class EjercicioAsignado(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fecha_asignada = models.DateTimeField(null=True)
    fecha_limite = models.DateTimeField(null=True)
    url_video_paciente = models.FileField(upload_to='storage/', null=True, blank=True)

    class Meta:
        db_table = 'Ejercicio_Asignado'

class Feedback(models.Model):
    fisioterapeuta = models.ForeignKey(Fisioterapeuta, on_delete=models.CASCADE)
    ejercicio_asignado = models.ForeignKey(EjercicioAsignado, on_delete=models.CASCADE, null=True, blank=True)
    feedback = models.TextField(null=True)

    class Meta:
        db_table = 'Feedback'

class SeguimientoIA(models.Model):
    feedback_ia = models.TextField(null=True)
    ejercicio_asignado = models.ForeignKey(EjercicioAsignado, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Seguimiento_IA'
