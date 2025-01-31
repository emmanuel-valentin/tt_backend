from django.db import models
from django.contrib.auth.models import User

class Expediente(models.Model):
    titulo = models.CharField(max_length=45, null=True)
    descripcion = models.TextField(null=True)

    class Meta:
        db_table = 'Expediente'

class Persona(models.Model):
    nombre = models.CharField(max_length=45, null=True)
    apellido_pat = models.CharField(max_length=45, null=True)
    apellido_mat = models.CharField(max_length=45, null=True)
    fecha = models.CharField(max_length=45, null=True)
    direccion = models.CharField(max_length=200, null=True)
    nacionalidad = models.CharField(max_length=45, null=True)
    telefono = models.CharField(max_length=45, null=True)
    foto_url = models.CharField(max_length=45, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Persona'

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expediente = models.OneToOneField(Expediente, on_delete=models.CASCADE)
    ocupacion = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'Paciente'

class Fisioterapeuta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=100, null=True)
    codigo_token = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'Fisioterapeuta'

class Estado(models.Model):
    estado = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'Estado'

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=45, null=True)
    tipo = models.CharField(max_length=45, null=True)
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

    class Meta:
        db_table = 'Ejercicio_Asignado'
        unique_together = ('paciente', 'ejercicio')

class Feedback(models.Model):
    fisioterapeuta = models.ForeignKey(Fisioterapeuta, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    feedback = models.TextField(null=True)

    class Meta:
        db_table = 'Feedback'

class FeedbackFisioterapeuta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Feedback_Fisioterapeuta'
        unique_together = ('paciente', 'feedback')

class SeguimientoIA(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    feedback_ia = models.TextField(null=True)
    url_video_paciente = models.URLField(max_length=200, null=True)

    class Meta:
        db_table = 'Seguimiento_IA'