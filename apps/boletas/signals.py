from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(pre_save, sender='boletas.Boleta')
def boleta_pagada_caja(sender, instance, **kwargs):
    """Cuando una boleta pasa a 'pagada', registra ingreso en la caja del día."""
    if not instance.pk:
        return  # boleta nueva, no hace nada aún

    try:
        anterior = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if anterior.estado != 'pagada' and instance.estado == 'pagada':
        _crear_ingreso_caja(instance)


def _crear_ingreso_caja(boleta):
    from apps.caja.models import SesionCaja, MovimientoCaja
    hoy = timezone.localdate()
    sesion = SesionCaja.objects.filter(fecha=hoy, cerrada=False).first()
    if not sesion:
        return  # no hay caja abierta hoy, no registra
    MovimientoCaja.objects.create(
        sesion=sesion,
        tipo='ingreso',
        descripcion=f'Pago Boleta #{boleta.numero} — {boleta.cliente.nombre}',
        monto=boleta.total,
        boleta=boleta,
    )
