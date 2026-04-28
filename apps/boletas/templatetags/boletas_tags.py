from django import template

register = template.Library()


@register.filter
def pesos(value):
    """Formatea un número como peso chileno: $1.234.567"""
    try:
        return f'${int(value):,}'.replace(',', '.')
    except (ValueError, TypeError):
        return '$0'


@register.filter
def signo_monto(value, tipo):
    """Prefija + o - según el tipo de movimiento."""
    try:
        monto = f'${int(value):,}'.replace(',', '.')
        return f'+{monto}' if tipo == 'ingreso' else f'-{monto}'
    except (ValueError, TypeError):
        return '$0'
