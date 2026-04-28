from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/lista.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(nombre__icontains=q) | qs.filter(rut__icontains=q)
        return qs


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:lista')


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:lista')


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/detalle.html'
    context_object_name = 'cliente'
