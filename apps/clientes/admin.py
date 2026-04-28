from django.contrib import admin
from .models import Cliente, Moto


class MotoInline(admin.TabularInline):
    model = Moto
    extra = 0
    fields = ['marca', 'modelo', 'anio', 'placa', 'km_actual']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'telefono', 'correo', 'creado']
    search_fields = ['nombre', 'rut', 'correo']
    inlines = [MotoInline]


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'anio', 'placa', 'cliente', 'km_actual']
    search_fields = ['marca', 'modelo', 'placa', 'cliente__nombre']
    list_filter = ['marca']
