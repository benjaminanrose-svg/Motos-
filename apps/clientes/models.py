from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nombre} ({self.rut})'
