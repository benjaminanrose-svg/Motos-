from django.contrib import admin
from .models import SesionCaja, MovimientoCaja


class MovimientoInline(admin.TabularInline):
    model = MovimientoCaja
    extra = 0
    readonly_fields = ['hora']


@admin.register(SesionCaja)
class SesionCajaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'monto_apertura', 'cerrada', 'hora_apertura']
    list_filter = ['cerrada']
    inlines = [MovimientoInline]


@admin.register(MovimientoCaja)
class MovimientoCajaAdmin(admin.ModelAdmin):
    list_display = ['sesion', 'tipo', 'descripcion', 'monto', 'hora']
    list_filter = ['tipo']
