from django import template
import re

register = template.Library()


@register.filter
def formato_rut(value):
    """Formatea un RUT: 12345678 -> 12.345.678-K"""
    if not value:
        return value
    rut = str(value).replace('.', '').replace('-', '').upper()
    if len(rut) < 2:
        return value
    cuerpo, dv = rut[:-1], rut[-1]
    cuerpo_fmt = f'{int(cuerpo):,}'.replace(',', '.')
    return f'{cuerpo_fmt}-{dv}'
