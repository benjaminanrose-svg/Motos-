from django import forms
from django.forms import inlineformset_factory
from .models import Boleta, ItemBoleta

_I = 'input-field'


class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['cliente', 'moto', 'estado', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': _I, 'id': 'id_cliente'}),
            'moto': forms.Select(attrs={'class': _I, 'id': 'id_moto'}),
            'estado': forms.Select(attrs={'class': _I}),
            'observaciones': forms.Textarea(attrs={'class': _I, 'rows': 2, 'placeholder': 'Notas adicionales...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moto'].required = False
        self.fields['moto'].empty_label = '— Sin moto asociada —'
        # Si ya hay un cliente seleccionado, filtrar motos
        cliente_id = None
        if self.instance and self.instance.pk and self.instance.cliente_id:
            cliente_id = self.instance.cliente_id
        elif self.data.get('cliente'):
            try:
                cliente_id = int(self.data['cliente'])
            except (ValueError, TypeError):
                pass
        if cliente_id:
            from apps.clientes.models import Moto
            self.fields['moto'].queryset = Moto.objects.filter(cliente_id=cliente_id)
        else:
            from apps.clientes.models import Moto
            self.fields['moto'].queryset = Moto.objects.none()


class ItemBoletaForm(forms.ModelForm):
    class Meta:
        model = ItemBoleta
        fields = ['tipo', 'descripcion', 'cantidad', 'precio_unitario']
        widgets = {
            'tipo': forms.Select(attrs={'class': _I}),
            'descripcion': forms.TextInput(attrs={'class': _I, 'placeholder': 'Descripción del ítem'}),
            'cantidad': forms.NumberInput(attrs={'class': _I + ' cantidad-field', 'min': 1, 'value': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': _I + ' precio-field', 'min': 0, 'placeholder': '0'}),
        }


ItemBoletaFormSet = inlineformset_factory(
    Boleta,
    ItemBoleta,
    form=ItemBoletaForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
