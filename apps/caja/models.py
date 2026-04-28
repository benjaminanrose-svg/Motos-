from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class SesionCaja(models.Model):
    fecha = models.DateField(unique=True)
    usuario_apertura = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='aperturas_caja'
    )
    monto_apertura = models.PositiveIntegerField(default=0)
    hora_apertura = models.DateTimeField(auto_now_add=True)
    hora_cierre = models.DateTimeField(null=True, blank=True)
    monto_cierre = models.PositiveIntegerField(null=True, blank=True)
    cerrada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Sesión de Caja'
        verbose_name_plural = 'Sesiones de Caja'

    def __str__(self):
        return f'Caja {self.fecha}'

    @property
    def saldo_actual(self):
        ingresos = self.movimientos.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
        egresos = self.movimientos.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
        return self.monto_apertura + ingresos - egresos


class MovimientoCaja(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
        ('retiro', 'Retiro'),
    ]

    sesion = models.ForeignKey(SesionCaja, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=255)
    monto = models.PositiveIntegerField()
    hora = models.DateTimeField(auto_now_add=True)
    boleta = models.ForeignKey(
        'boletas.Boleta', on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ['-hora']
        verbose_name = 'Movimiento de Caja'
        verbose_name_plural = 'Movimientos de Caja'

    def __str__(self):
        return f'{self.get_tipo_display()} ${self.monto:,} — {self.descripcion}'
