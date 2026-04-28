from django.db import models


class ConfiguracionTaller(models.Model):
    """Singleton: solo existe un registro con los datos del taller."""
    nombre = models.CharField(max_length=150, default='MotoTaller')
    rut = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    horario = models.CharField(max_length=200, blank=True, help_text='Ej: Lun–Vie 9:00–18:30 / Sáb 9:00–14:00')
    logo = models.ImageField(upload_to='taller/', blank=True, null=True)
    mensaje_pie_boleta = models.CharField(max_length=255, blank=True, default='¡Gracias por su preferencia!')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Configuración del Taller'
        verbose_name_plural = 'Configuración del Taller'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.pk = 1  # forzar singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
