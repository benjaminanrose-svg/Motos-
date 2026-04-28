from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import SesionCaja, MovimientoCaja
from .forms import AperturaCajaForm, MovimientoCajaForm


class CajaDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'caja/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        ctx['sesion_hoy'] = SesionCaja.objects.filter(fecha=hoy).first()
        ctx['sesiones_recientes'] = SesionCaja.objects.order_by('-fecha')[:7]
        return ctx


class CajaSesionDetailView(LoginRequiredMixin, DetailView):
    model = SesionCaja
    template_name = 'caja/sesion_detalle.html'
    context_object_name = 'sesion'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('movimientos')


@login_required
def abrir_caja(request):
    hoy = timezone.localdate()
    if SesionCaja.objects.filter(fecha=hoy).exists():
        messages.warning(request, 'Ya existe una caja abierta para hoy.')
        return redirect('caja:dashboard')
    form = AperturaCajaForm(request.POST or None)
    if form.is_valid():
        sesion = form.save(commit=False)
        sesion.fecha = hoy
        sesion.usuario_apertura = request.user
        sesion.save()
        messages.success(request, f'Caja abierta con monto inicial ${sesion.monto_apertura:,}')
        return redirect('caja:sesion', pk=sesion.pk)
    return redirect('caja:dashboard')


@login_required
def cerrar_caja(request, pk):
    sesion = get_object_or_404(SesionCaja, pk=pk, cerrada=False)
    sesion.cerrada = True
    sesion.hora_cierre = timezone.now()
    sesion.monto_cierre = sesion.saldo_actual
    sesion.save()
    messages.success(request, f'Caja cerrada. Saldo final: ${sesion.monto_cierre:,}')
    return redirect('caja:dashboard')


@login_required
def agregar_movimiento(request, pk):
    sesion = get_object_or_404(SesionCaja, pk=pk, cerrada=False)
    form = MovimientoCajaForm(request.POST or None)
    if form.is_valid():
        mov = form.save(commit=False)
        mov.sesion = sesion
        mov.save()
        messages.success(request, 'Movimiento registrado.')
    return redirect('caja:sesion', pk=sesion.pk)
