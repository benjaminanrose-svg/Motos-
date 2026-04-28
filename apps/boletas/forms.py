from django import forms
from django.forms import inlineformset_factory
from .models import Boleta, ItemBoleta


class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['cliente', 'estado', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'input-field'}),
            'estado': forms.Select(attrs={'class': 'input-field'}),
            'observaciones': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
        }


class ItemBoletaForm(forms.ModelForm):
    class Meta:
        model = ItemBoleta
        fields = ['tipo', 'descripcion', 'cantidad', 'precio_unitario']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'input-field'}),
            'descripcion': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Descripción'}),
            'cantidad': forms.NumberInput(attrs={'class': 'input-field', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'input-field', 'min': 0}),
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
