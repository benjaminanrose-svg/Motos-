from django import forms
from .models import SesionCaja, MovimientoCaja


class AperturaCajaForm(forms.ModelForm):
    class Meta:
        model = SesionCaja
        fields = ['monto_apertura']
        widgets = {
            'monto_apertura': forms.NumberInput(attrs={'class': 'input-field', 'min': 0, 'placeholder': 'Monto inicial'}),
        }


class MovimientoCajaForm(forms.ModelForm):
    class Meta:
        model = MovimientoCaja
        fields = ['tipo', 'descripcion', 'monto']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'input-field'}),
            'descripcion': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Descripción del movimiento'}),
            'monto': forms.NumberInput(attrs={'class': 'input-field', 'min': 1, 'placeholder': 'Monto en pesos'}),
        }
