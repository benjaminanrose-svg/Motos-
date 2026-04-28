from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
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

        sesion_hoy = SesionCaja.objects.filter(fecha=hoy).first()
        ctx['sesion_hoy'] = sesion_hoy
        ctx['saldo_caja'] = sesion_hoy.saldo_actual if sesion_hoy else 0

        movs_mes = MovimientoCaja.objects.filter(
            hora__year=hoy.year, hora__month=hoy.month
        )
        ingresos = movs_mes.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
        egresos = movs_mes.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
        ctx['balance_mes'] = ingresos - egresos

        ctx['ultimas_boletas'] = Boleta.objects.select_related('cliente').order_by('-fecha_emision')[:5]
        ctx['ultimos_movimientos'] = (
            sesion_hoy.movimientos.order_by('-hora')[:5] if sesion_hoy else []
        )
        return ctx
