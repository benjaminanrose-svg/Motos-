from django.views.generic import TemplateView
from .models import Servicio


class LandingView(TemplateView):
    template_name = 'publico/landing.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['servicios'] = Servicio.objects.filter(activo=True)
        return ctx
