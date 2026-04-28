import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Cliente, Moto
from .forms import ClienteForm, MotoForm


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/lista.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(rut__icontains=q) | Q(correo__icontains=q))
        return qs


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        from django.contrib import messages
        messages.success(self.request, 'Cliente creado correctamente.')
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        from django.contrib import messages
        messages.success(self.request, 'Cliente actualizado.')
        return super().form_valid(form)


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/detalle.html'
    context_object_name = 'cliente'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('motos', 'boletas__items')


# ── Motos ─────────────────────────────────────────────────────────────────────

class MotoCreateView(LoginRequiredMixin, CreateView):
    model = Moto
    form_class = MotoForm
    template_name = 'clientes/moto_form.html'

    def get_initial(self):
        return {'cliente': self.kwargs.get('cliente_pk')}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cliente'] = Cliente.objects.get(pk=self.kwargs['cliente_pk'])
        return ctx

    def form_valid(self, form):
        from django.contrib import messages
        messages.success(self.request, 'Moto registrada.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('clientes:detalle', kwargs={'pk': self.object.cliente_id})


class MotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Moto
    form_class = MotoForm
    template_name = 'clientes/moto_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cliente'] = self.object.cliente
        return ctx

    def get_success_url(self):
        return reverse_lazy('clientes:detalle', kwargs={'pk': self.object.cliente_id})


class MotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Moto
    template_name = 'clientes/moto_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('clientes:detalle', kwargs={'pk': self.object.cliente_id})


def form_cliente_pk(view):
    if hasattr(view, 'object') and view.object:
        return view.object.cliente_id
    return view.kwargs.get('cliente_pk')


# ── AJAX ──────────────────────────────────────────────────────────────────────

@login_required
def cliente_search_ajax(request):
    """Devuelve JSON con clientes que coinciden con el término de búsqueda."""
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})
    clientes = Cliente.objects.filter(
        Q(nombre__icontains=q) | Q(rut__icontains=q)
    )[:10]
    data = [{'id': c.pk, 'text': f'{c.nombre} — {c.rut}'} for c in clientes]
    return JsonResponse({'results': data})


@login_required
def cliente_motos_ajax(request, pk):
    """Devuelve las motos de un cliente para el selector dinámico en boletas."""
    motos = Moto.objects.filter(cliente_id=pk)
    data = [
        {'id': m.pk, 'marca': m.marca, 'modelo': m.modelo, 'anio': m.anio, 'placa': m.placa}
        for m in motos
    ]
    return JsonResponse(data, safe=False)


# ── CSV Export ─────────────────────────────────────────────────────────────────

@login_required
def clientes_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
    response.write('﻿')  # BOM para Excel
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'RUT', 'Teléfono', 'Correo', 'Dirección', 'Fecha registro', 'Boletas'])
    for c in Cliente.objects.all():
        writer.writerow([
            c.nombre, c.rut, c.telefono, c.correo, c.direccion,
            c.creado.strftime('%d/%m/%Y'),
            c.boletas.count(),
        ])
    return response
