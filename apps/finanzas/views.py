from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from datetime import date, timedelta
import json
from apps.caja.models import MovimientoCaja


class FinanzasDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'finanzas/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()

        # Rango seleccionado por el usuario
        rango = self.request.GET.get('rango', 'mes')
        fecha_desde, fecha_hasta = _rango_fechas(hoy, rango)
        ctx['rango'] = rango
        ctx['fecha_desde'] = fecha_desde
        ctx['fecha_hasta'] = fecha_hasta
        ctx['rango_opciones'] = [
            ('semana', 'Semana'),
            ('mes', 'Mes'),
            ('trimestre', 'Trimestre'),
            ('año', 'Año'),
        ]

        # Totales del período
        movs = MovimientoCaja.objects.filter(
            hora__date__gte=fecha_desde,
            hora__date__lte=fecha_hasta,
        )
        ctx['ingresos_periodo'] = movs.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
        ctx['egresos_periodo'] = movs.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
        ctx['balance_periodo'] = ctx['ingresos_periodo'] - ctx['egresos_periodo']

        # Totales del año actual
        movs_año = MovimientoCaja.objects.filter(hora__year=hoy.year)
        ctx['ingresos_año'] = movs_año.filter(tipo='ingreso').aggregate(s=Sum('monto'))['s'] or 0
        ctx['egresos_año'] = movs_año.filter(tipo__in=['egreso', 'retiro']).aggregate(s=Sum('monto'))['s'] or 0
        ctx['balance_año'] = ctx['ingresos_año'] - ctx['egresos_año']
        ctx['año_actual'] = hoy.year

        # Datos Chart.js — últimos 12 meses
        labels, ingresos_chart, egresos_chart = [], [], []
        for i in range(11, -1, -1):
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
            labels.append(date(año, mes, 1).strftime('%b %y'))
            ingresos_chart.append(ing)
            egresos_chart.append(egr)

        ctx['chart_labels'] = json.dumps(labels)
        ctx['chart_ingresos'] = json.dumps(ingresos_chart)
        ctx['chart_egresos'] = json.dumps(egresos_chart)

        # Últimos movimientos del período
        ctx['ultimos_movimientos'] = movs.select_related('sesion').order_by('-hora')[:20]
        return ctx


def _rango_fechas(hoy, rango):
    if rango == 'semana':
        return hoy - timedelta(days=6), hoy
    elif rango == 'mes':
        return hoy.replace(day=1), hoy
    elif rango == 'trimestre':
        mes_inicio = ((hoy.month - 1) // 3) * 3 + 1
        return hoy.replace(month=mes_inicio, day=1), hoy
    elif rango == 'año':
        return hoy.replace(month=1, day=1), hoy
    return hoy.replace(day=1), hoy
