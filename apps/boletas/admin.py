from django.contrib import admin
from .models import Boleta, ItemBoleta


class ItemBoletaInline(admin.TabularInline):
    model = ItemBoleta
    extra = 1


@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'fecha_emision', 'estado']
    list_filter = ['estado', 'fecha_emision']
    search_fields = ['numero', 'cliente__nombre']
    inlines = [ItemBoletaInline]
