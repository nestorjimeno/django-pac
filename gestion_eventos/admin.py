from typing import Any
from django.contrib import admin
from .models import Evaluacion, Evento, Accion
from .forms import EventoForm


class EventoAdmin(admin.ModelAdmin):
    form = EventoForm  # Usar el formulario personalizado
    
    # Campos que estarán en solo lectura al visualizar el evento en el admin
    readonly_fields = ('usuario_alta', 'fecha_estado',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario_alta = request.user
        return super().save_model(request, obj, form, change)

    


admin.site.register(Evaluacion)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Accion)
