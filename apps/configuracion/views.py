from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ConfiguracionTaller
from .forms import ConfiguracionTallerForm


class ConfiguracionView(LoginRequiredMixin, UpdateView):
    model = ConfiguracionTaller
    form_class = ConfiguracionTallerForm
    template_name = 'configuracion/form.html'
    success_url = reverse_lazy('configuracion:editar')

    def get_object(self, queryset=None):
        return ConfiguracionTaller.get()

    def form_valid(self, form):
        messages.success(self.request, 'Configuración guardada correctamente.')
        return super().form_valid(form)
