from django import forms
from .models import Cliente


def validar_rut(rut_raw: str) -> str:
    """Valida y retorna el RUT limpio (sin puntos, con guión). Lanza ValidationError si es inválido."""
    rut = rut_raw.strip().upper().replace('.', '').replace(' ', '')
    if '-' not in rut:
        raise forms.ValidationError('Ingresa el RUT con guión (ej: 12345678-9).')
    cuerpo, dv = rut.rsplit('-', 1)
    if not cuerpo.isdigit():
        raise forms.ValidationError('El cuerpo del RUT debe contener solo dígitos.')
    n = int(cuerpo)
    if n < 1_000_000:
        raise forms.ValidationError('RUT demasiado corto.')

    # Algoritmo módulo 11
    suma, mult = 0, 2
    for d in reversed(str(n)):
        suma += int(d) * mult
        mult = 2 if mult == 7 else mult + 1
    resto = 11 - (suma % 11)
    dv_esperado = 'K' if resto == 10 else ('0' if resto == 11 else str(resto))

    if dv != dv_esperado:
        raise forms.ValidationError(f'RUT inválido. El dígito verificador correcto es {dv_esperado}.')
    return rut  # retorna en formato NNNNNNNN-D


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'rut', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input-field', 'placeholder': 'Nombre completo',
            }),
            'rut': forms.TextInput(attrs={
                'class': 'input-field', 'placeholder': 'Ej: 12345678-9',
                'data-rut': 'true',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'input-field', 'placeholder': '+56 9 1234 5678',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'input-field', 'placeholder': 'correo@ejemplo.cl',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'input-field', 'placeholder': 'Dirección',
            }),
        }

    def clean_rut(self):
        return validar_rut(self.cleaned_data['rut'])
