from django.apps import AppConfig

class BoletasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.boletas'

    def ready(self):
        import apps.boletas.signals  # noqa: F401
