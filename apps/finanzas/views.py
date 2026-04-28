from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from datetime import date
from apps.caja.models import MovimientoCaja, SesionCaja


class FinanzasDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'finanzas/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        año_actual = hoy.year
        mes_actual = hoy.month

        # Totales del mes actual
        movs_mes = MovimientoCaja.objects.filter(
            hora__year=año_actual,
            hora__month=mes_actual,
        )
        ctx['ingresos_mes'] = movs_mes.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
        ctx['egresos_mes'] = movs_mes.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
        ctx['balance_mes'] = ctx['ingresos_mes'] - ctx['egresos_mes']

        # Totales del año actual
        movs_año = MovimientoCaja.objects.filter(hora__year=año_actual)
        ctx['ingresos_año'] = movs_año.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
        ctx['egresos_año'] = movs_año.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
        ctx['balance_año'] = ctx['ingresos_año'] - ctx['egresos_año']

        # Datos por mes para gráfico (últimos 6 meses)
        ctx['datos_meses'] = self._datos_ultimos_meses(6)
        ctx['año_actual'] = año_actual
        ctx['mes_actual'] = mes_actual
        return ctx

    def _datos_ultimos_meses(self, n):
        hoy = timezone.localdate()
        resultado = []
        for i in range(n - 1, -1, -1):
            mes = hoy.month - i
            año = hoy.year
            while mes < 1:
                mes += 12
                año -= 1
            ingresos = MovimientoCaja.objects.filter(
                hora__year=año, hora__month=mes, tipo='ingreso'
            ).aggregate(s=Sum('monto'))['s'] or 0
            egresos = MovimientoCaja.objects.filter(
                hora__year=año, hora__month=mes, tipo__in=['egreso', 'retiro']
            ).aggregate(s=Sum('monto'))['s'] or 0
            resultado.append({
                'mes': date(año, mes, 1).strftime('%b %Y'),
                'ingresos': ingresos,
                'egresos': egresos,
            })
        return resultado
