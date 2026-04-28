from django.contrib import admin
from .models import ConfiguracionTaller


@admin.register(ConfiguracionTaller)
class ConfiguracionTallerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos del taller', {'fields': ('nombre', 'rut', 'logo')}),
        ('Contacto', {'fields': ('direccion', 'telefono', 'email', 'horario')}),
        ('Boletas', {'fields': ('mensaje_pie_boleta',)}),
    )

    def has_add_permission(self, request):
        return not ConfiguracionTaller.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
