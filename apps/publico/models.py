from django.db import models


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='wrench')
    activo = models.BooleanField(default=True)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre
