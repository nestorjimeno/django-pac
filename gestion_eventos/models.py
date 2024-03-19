from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Evento(models.Model):

    titulo = models.CharField("Título", max_length=250)
    fecha_alta = models.DateField("Fecha de alta", auto_now=False, auto_now_add=True, editable=False)
    fecha_evento = models.DateField("Fecha del evento", auto_now=False, auto_now_add=False)
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    ]
    estado = models.CharField('Estado', max_length=10, choices=ESTADO_CHOICES)
    fecha_estado = models.DateField("Fecha del estado", auto_now=False, auto_now_add=False, editable=False, blank=True)
    descripcion = models.TextField("Descripción")
    clasificaciones = {
        'GRAVE': 'NIVEL 1',
        'LEVE': 'NIVEL 2',
    }
    clasificacion = models.CharField("Clasificación", max_length=50, choices=clasificaciones)
    usuario_alta = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuario que da de alta", on_delete=models.CASCADE, related_name='+', editable=False, null=True, blank=True)
    evaluacion = models.ForeignKey("Evaluacion", verbose_name="Evaluación", on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    responsable_cierre = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Responsable de cierre", on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name = "evento"
        verbose_name_plural = "eventos"
    
    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("evaluacion_detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        if 'estado' in self.changed_fields():
            self.fecha_estado = timezone.now().date()
            print('**** ESTADO ACTUALIZADO ****')
        return super(Evento, self).save(*args, **kwargs)
    
    def changed_fields(self):
        """
        Método auxiliar para obtener los campos que han cambiado en el modelo.
        """
        changed = []
        if self.pk is None:
            return self.__dict__.keys()
        old = self.__class__.objects.get(pk=self.pk)
        for field in self.__dict__.keys():
            if getattr(self, field) != getattr(old, field):
                changed.append(field)
        return changed

class Evaluacion(models.Model):

    evento_asociado = models.ForeignKey("Evento", verbose_name="Evento", on_delete=models.CASCADE, related_name='+')
    evaluador = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Evaluador", on_delete=models.CASCADE, related_name='+')
    texto_evaluacion = models.TextField("Evaluación")
    causas_choices = {
        'CAUSA-A': 'CAUSA-A',
        'CAUSA-B': 'CAUSA-B',

    }
    causas = models.CharField("Causas", max_length=250, choices=causas_choices)
    eventos_repetitivos = models.ManyToManyField("Evento", verbose_name="Eventos repetitivos", related_name='+')
    acciones = models.ManyToManyField("Accion", verbose_name="Acciones")

    class Meta:
        verbose_name = "evaluación"
        verbose_name_plural = "evaluaciones"

    def __str__(self):
        return 'Evaluación del evento ' + self.evento

    def get_absolute_url(self):
        return reverse("evaluacion_detail", kwargs={"pk": self.pk})
    

class Accion(models.Model):

    titulo = models.CharField("Título", max_length=250)
    evento_asociado = models.ForeignKey("Evento", verbose_name="Evento", on_delete=models.CASCADE, related_name='+')
    fecha_alta = models.DateField("Fecha de alta", auto_now=False, auto_now_add=True)
    estados = {
        'ABIERTO': 'ABIERTO',
        'CERRADO': 'CERRADO',
    }
    estado = models.CharField("Estado", max_length=50, choices=estados)
    fecha_estado = models.DateField("Fecha del estado", auto_now=False, auto_now_add=False)
    fecha_limite = models.DateField("Fecha de cierre", auto_now=False, auto_now_add=False)
    fecha_cierre = models.DateField("Fecha de cierre", auto_now=False, auto_now_add=False)
    descripción = models.TextField("Descripción")
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Responsable", on_delete=models.CASCADE, related_name='+')
    
    class Meta:
        verbose_name = "Accion"
        verbose_name_plural = "Acciones"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("Accion_detail", kwargs={"pk": self.pk})

