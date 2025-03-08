from django.contrib import admin

from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'profissional', 'data')
    search_fields = ('cliente__nome', 'profissional__nome')
    list_filter = ('data',)
