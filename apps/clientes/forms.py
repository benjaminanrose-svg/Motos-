from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'rut', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Nombre completo'}),
            'rut': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ej: 12.345.678-9'}),
            'telefono': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '+56 9 XXXX XXXX'}),
            'correo': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'correo@ejemplo.cl'}),
            'direccion': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Dirección'}),
        }
