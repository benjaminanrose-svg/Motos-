import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib import messages
from weasyprint import HTML
from .models import Boleta, ItemBoleta
from .forms import BoletaForm, ItemBoletaFormSet


class BoletaListView(LoginRequiredMixin, ListView):
    model = Boleta
    template_name = 'boletas/lista.html'
    context_object_name = 'boletas'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('cliente')
        q = self.request.GET.get('q', '')
        estado = self.request.GET.get('estado', '')
        if q:
            qs = qs.filter(cliente__nombre__icontains=q) | qs.filter(numero__icontains=q)
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['estado_choices'] = Boleta.ESTADO_CHOICES
        ctx['estado_actual'] = self.request.GET.get('estado', '')
        return ctx


class BoletaCreateView(LoginRequiredMixin, CreateView):
    model = Boleta
    form_class = BoletaForm
    template_name = 'boletas/form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['formset'] = (
            ItemBoletaFormSet(self.request.POST) if self.request.POST
            else ItemBoletaFormSet()
        )
        return ctx

    def form_valid(self, form):
        formset = ItemBoletaFormSet(self.request.POST)
        if not formset.is_valid():
            return self.form_invalid(form)
        ultimo = Boleta.objects.order_by('-numero').first()
        form.instance.numero = (ultimo.numero + 1) if ultimo else 1
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        messages.success(self.request, f'Boleta #{self.object.numero} creada correctamente.')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('boletas:detalle', kwargs={'pk': self.object.pk})


class BoletaDetailView(LoginRequiredMixin, DetailView):
    model = Boleta
    template_name = 'boletas/detalle.html'
    context_object_name = 'boleta'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('items').select_related('cliente', 'moto')


class BoletaUpdateView(LoginRequiredMixin, UpdateView):
    model = Boleta
    form_class = BoletaForm
    template_name = 'boletas/form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['formset'] = (
            ItemBoletaFormSet(self.request.POST, instance=self.object) if self.request.POST
            else ItemBoletaFormSet(instance=self.object)
        )
        return ctx

    def form_valid(self, form):
        formset = ItemBoletaFormSet(self.request.POST, instance=self.object)
        if not formset.is_valid():
            return self.form_invalid(form)
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        messages.success(self.request, f'Boleta #{self.object.numero} actualizada.')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('boletas:detalle', kwargs={'pk': self.object.pk})


@login_required
def boleta_pagar(request, pk):
    """Marca la boleta como pagada y genera ingreso en caja (via signal)."""
    boleta = get_object_or_404(Boleta, pk=pk)
    if boleta.estado in ('pagada', 'anulada'):
        messages.warning(request, f'La boleta ya está en estado {boleta.get_estado_display()}.')
    else:
        boleta.marcar_pagada()
        messages.success(request, f'Boleta #{boleta.numero} marcada como pagada. Ingreso registrado en caja.')
    return redirect('boletas:detalle', pk=pk)


@login_required
def boleta_anular(request, pk):
    boleta = get_object_or_404(Boleta, pk=pk)
    if boleta.estado == 'anulada':
        messages.warning(request, 'La boleta ya está anulada.')
    else:
        boleta.estado = 'anulada'
        boleta.save()
        messages.success(request, f'Boleta #{boleta.numero} anulada.')
    return redirect('boletas:detalle', pk=pk)


@login_required
def boleta_pdf(request, pk):
    boleta = get_object_or_404(
        Boleta.objects.prefetch_related('items').select_related('cliente', 'moto'), pk=pk
    )
    from apps.configuracion.models import ConfiguracionTaller
    taller = ConfiguracionTaller.get()
    html_string = render_to_string('boletas/pdf.html', {'boleta': boleta, 'taller': taller})
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="boleta_{boleta.numero}.pdf"'
    return response


@login_required
def boletas_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="boletas.csv"'
    response.write('﻿')  # BOM para Excel
    writer = csv.writer(response)
    writer.writerow(['Número', 'Cliente', 'RUT', 'Fecha', 'Estado', 'Subtotal', 'IVA', 'Total'])
    for b in Boleta.objects.select_related('cliente').order_by('-numero'):
        writer.writerow([
            b.numero, b.cliente.nombre, b.cliente.rut,
            b.fecha_emision.strftime('%d/%m/%Y'),
            b.get_estado_display(),
            b.subtotal, b.iva, b.total,
        ])
    return response
