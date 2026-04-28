from django.db import models
from django.db.models import Sum
from apps.clientes.models import Cliente


class Boleta(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitida', 'Emitida'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada'),
    ]

    numero = models.PositiveIntegerField(unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='boletas')
    fecha_emision = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='borrador')
    observaciones = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_emision', '-numero']
        verbose_name = 'Boleta'
        verbose_name_plural = 'Boletas'

    def __str__(self):
        return f'Boleta #{self.numero} - {self.cliente.nombre}'

    @property
    def subtotal(self):
        return self.items.aggregate(s=Sum('subtotal'))['s'] or 0

    @property
    def iva(self):
        return round(self.subtotal * 19 / 100)

    @property
    def total(self):
        return self.subtotal + self.iva


class ItemBoleta(models.Model):
    TIPO_CHOICES = [
        ('servicio', 'Servicio'),
        ('repuesto', 'Repuesto'),
    ]

    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE, related_name='items')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='servicio')
    descripcion = models.CharField(max_length=255)
    cantidad = models.PositiveSmallIntegerField(default=1)
    precio_unitario = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Ítem de Boleta'
        verbose_name_plural = 'Ítems de Boleta'

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.descripcion} x{self.cantidad}'
