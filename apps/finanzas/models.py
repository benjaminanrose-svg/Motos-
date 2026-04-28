from django.db import models


class Categoria(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    class Meta:
        ordering = ['tipo', 'nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return f'{self.nombre} ({self.get_tipo_display()})'
