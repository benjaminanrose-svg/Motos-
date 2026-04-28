from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.utils import timezone
from django.shortcuts import render
from apps.clientes.models import Cliente
from apps.boletas.models import Boleta
from apps.caja.models import SesionCaja, MovimientoCaja


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()

        ctx['total_clientes'] = Cliente.objects.count()
        ctx['boletas_mes'] = Boleta.objects.filter(
            fecha_emision__year=hoy.year,
            fecha_emision__month=hoy.month,
        ).exclude(estado='anulada').count()
        ctx['boletas_pendientes'] = Boleta.objects.filter(estado__in=['borrador', 'emitida']).count()

        sesion_hoy = SesionCaja.objects.filter(fecha=hoy).first()
        ctx['sesion_hoy'] = sesion_hoy
        ctx['saldo_caja'] = sesion_hoy.saldo_actual if sesion_hoy else 0

        movs_mes = MovimientoCaja.objects.filter(hora__year=hoy.year, hora__month=hoy.month)
        ingresos = movs_mes.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
        egresos = movs_mes.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
        ctx['balance_mes'] = ingresos - egresos
        ctx['ingresos_mes'] = ingresos
        ctx['egresos_mes'] = egresos

        ctx['ultimas_boletas'] = (
            Boleta.objects.select_related('cliente').order_by('-fecha_emision', '-numero')[:8]
        )
        ctx['ultimos_movimientos'] = (
            sesion_hoy.movimientos.order_by('-hora')[:6] if sesion_hoy else []
        )

        # Datos para mini chart del sidebar (últimos 6 meses)
        ctx['chart_labels'], ctx['chart_ingresos'], ctx['chart_egresos'] = _datos_chart(6)
        return ctx


def _datos_chart(n):
    from datetime import date
    hoy = timezone.localdate()
    labels, ingresos_list, egresos_list = [], [], []
    for i in range(n - 1, -1, -1):
        mes = hoy.month - i
        año = hoy.year
        while mes < 1:
            mes += 12
            año -= 1
        ing = MovimientoCaja.objects.filter(
            hora__year=año, hora__month=mes, tipo='ingreso'
        ).aggregate(s=Sum('monto'))['s'] or 0
        egr = MovimientoCaja.objects.filter(
            hora__year=año, hora__month=mes, tipo__in=['egreso', 'retiro']
        ).aggregate(s=Sum('monto'))['s'] or 0
        labels.append(date(año, mes, 1).strftime('%b'))
        ingresos_list.append(ing)
        egresos_list.append(egr)
    return labels, ingresos_list, egresos_list


def error_404(request, exception=None):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)
