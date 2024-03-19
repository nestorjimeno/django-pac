from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        exclude = ('usuario_alta', 'fecha_estado',)  # Excluimos el campo fecha_estado del formulario de creación
