from django import forms
from .models import ConfiguracionTaller


class ConfiguracionTallerForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionTaller
        fields = ['nombre', 'rut', 'direccion', 'telefono', 'email', 'horario', 'logo', 'mensaje_pie_boleta']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-field'}),
            'rut': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ej: 76.123.456-7'}),
            'direccion': forms.TextInput(attrs={'class': 'input-field'}),
            'telefono': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'horario': forms.TextInput(attrs={'class': 'input-field'}),
            'mensaje_pie_boleta': forms.TextInput(attrs={'class': 'input-field'}),
        }
