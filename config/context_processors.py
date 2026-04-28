def taller(request):
    """Inyecta la configuración del taller en todos los templates."""
    from apps.configuracion.models import ConfiguracionTaller
    try:
        return {'taller': ConfiguracionTaller.get()}
    except Exception:
        return {'taller': None}
