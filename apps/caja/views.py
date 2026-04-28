from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView
from django.db.models import Sum
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
        sesion_hoy = SesionCaja.objects.filter(fecha=hoy).first()
        ctx['sesion_hoy'] = sesion_hoy
        ctx['sesiones_recientes'] = SesionCaja.objects.order_by('-fecha')[:10]
        ctx['form_apertura'] = AperturaCajaForm()

        if sesion_hoy:
            movs = sesion_hoy.movimientos.all()
            ctx['total_ingresos'] = movs.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
            ctx['total_egresos'] = movs.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
            ctx['form_movimiento'] = MovimientoCajaForm()
        return ctx


class CajaSesionDetailView(LoginRequiredMixin, DetailView):
    model = SesionCaja
    template_name = 'caja/sesion_detalle.html'
    context_object_name = 'sesion'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_movimiento'] = MovimientoCajaForm()
        movs = self.object.movimientos.all()
        ctx['total_ingresos'] = movs.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
        ctx['total_egresos'] = movs.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
        return ctx

    def get_queryset(self):
        return super().get_queryset().prefetch_related('movimientos')


@login_required
def abrir_caja(request):
    if request.method != 'POST':
        return redirect('caja:dashboard')
    hoy = timezone.localdate()
    if SesionCaja.objects.filter(fecha=hoy).exists():
        messages.warning(request, 'Ya existe una caja abierta para hoy.')
        return redirect('caja:dashboard')
    form = AperturaCajaForm(request.POST)
    if form.is_valid():
        sesion = form.save(commit=False)
        sesion.fecha = hoy
        sesion.usuario_apertura = request.user
        sesion.save()
        messages.success(request, f'Caja abierta. Monto inicial: ${sesion.monto_apertura:,}')
        return redirect('caja:sesion', pk=sesion.pk)
    messages.error(request, 'Error al abrir la caja.')
    return redirect('caja:dashboard')


@login_required
def cerrar_caja(request, pk):
    if request.method != 'POST':
        return redirect('caja:dashboard')
    sesion = get_object_or_404(SesionCaja, pk=pk, cerrada=False)
    sesion.cerrada = True
    sesion.hora_cierre = timezone.now()
    sesion.monto_cierre = sesion.saldo_actual
    sesion.save()
    messages.success(request, f'Caja cerrada. Saldo final: ${sesion.monto_cierre:,}')
    return redirect('caja:dashboard')


@login_required
def agregar_movimiento(request, pk):
    if request.method != 'POST':
        return redirect('caja:sesion', pk=pk)
    sesion = get_object_or_404(SesionCaja, pk=pk, cerrada=False)
    form = MovimientoCajaForm(request.POST)
    if form.is_valid():
        mov = form.save(commit=False)
        mov.sesion = sesion
        mov.save()
        messages.success(request, f'{mov.get_tipo_display()} registrado: ${mov.monto:,}')
    else:
        messages.error(request, 'Datos inválidos en el movimiento.')
    return redirect('caja:sesion', pk=sesion.pk)
