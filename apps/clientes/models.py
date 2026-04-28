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


class Moto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='motos')
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=80)
    anio = models.PositiveSmallIntegerField(verbose_name='Año')
    placa = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=40, blank=True)
    vin = models.CharField(max_length=20, blank=True, verbose_name='VIN / Nº Motor')
    km_actual = models.PositiveIntegerField(default=0, verbose_name='Kilometraje actual')
    observaciones = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['marca', 'modelo']
        verbose_name = 'Moto'
        verbose_name_plural = 'Motos'

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.anio}) — {self.cliente.nombre}'
