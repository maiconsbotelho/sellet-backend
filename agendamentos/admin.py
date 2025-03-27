from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Agendamento

# Filtro por dia
class DiaAgendamentoFilter(admin.SimpleListFilter):
    title = 'Dia'
    parameter_name = 'dia_agendamento'

    def lookups(self, request, model_admin):
        return (
            ('hoje', 'Hoje'),
            ('ontem', 'Ontem'),
            ('esta_semana', 'Esta Semana'),
            ('este_mes', 'Este Mês'),
            ('proxima_semana', 'Próxima Semana'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'hoje':
            today = timezone.now().date()
            return queryset.filter(data=today)
        elif self.value() == 'ontem':
            yesterday = timezone.now().date() - timedelta(days=1)
            return queryset.filter(data=yesterday)
        elif self.value() == 'esta_semana':
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())  # Segunda-feira
            end_of_week = start_of_week + timedelta(days=6)  # Domingo
            return queryset.filter(data__gte=start_of_week, data__lte=end_of_week)
        elif self.value() == 'este_mes':
            today = timezone.now().date()
            return queryset.filter(data__month=today.month, data__year=today.year)
        elif self.value() == 'proxima_semana':
            today = timezone.now().date()
            start_of_next_week = today + timedelta(days=(7 - today.weekday()))  # Próxima segunda-feira
            end_of_next_week = start_of_next_week + timedelta(days=6)  # Próximo domingo
            return queryset.filter(data__gte=start_of_next_week, data__lte=end_of_next_week)
        return queryset

# Filtro por semana
class SemanaAgendamentoFilter(admin.SimpleListFilter):
    title = 'Semana'
    parameter_name = 'semana_agendamento'

    def lookups(self, request, model_admin):
        return (
            ('esta_semana', 'Esta Semana'),
            ('ultima_semana', 'Última Semana'),
            ('proxima_semana', 'Próxima Semana'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'esta_semana':
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())  # Segunda-feira
            end_of_week = start_of_week + timedelta(days=6)  # Domingo
            return queryset.filter(data__gte=start_of_week, data__lte=end_of_week)
        elif self.value() == 'ultima_semana':
            today = timezone.now().date()
            start_of_last_week = today - timedelta(days=today.weekday() + 7)  # Segunda-feira da semana passada
            end_of_last_week = start_of_last_week + timedelta(days=6)  # Domingo da semana passada
            return queryset.filter(data__gte=start_of_last_week, data__lte=end_of_last_week)
        elif self.value() == 'proxima_semana':
            today = timezone.now().date()
            start_of_next_week = today + timedelta(days=(7 - today.weekday()))  # Próxima segunda-feira
            end_of_next_week = start_of_next_week + timedelta(days=6)  # Próximo domingo
            return queryset.filter(data__gte=start_of_next_week, data__lte=end_of_next_week)
        return queryset

# Filtro por mês
class MesAgendamentoFilter(admin.SimpleListFilter):
    title = 'Mês'
    parameter_name = 'mes_agendamento'

    def lookups(self, request, model_admin):
        return (
            ('este_mes', 'Este Mês'),
            ('ultimo_mes', 'Último Mês'),
            ('proximo_mes', 'Próximo Mês'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'este_mes':
            today = timezone.now().date()
            return queryset.filter(data__month=today.month, data__year=today.year)
        elif self.value() == 'ultimo_mes':
            today = timezone.now().date()
            last_month = today.replace(month=today.month-1) if today.month > 1 else today.replace(month=12, year=today.year-1)
            return queryset.filter(data__month=last_month.month, data__year=last_month.year)
        elif self.value() == 'proximo_mes':
            today = timezone.now().date()
            next_month = today.replace(month=today.month+1) if today.month < 12 else today.replace(month=1, year=today.year+1)
            return queryset.filter(data__month=next_month.month, data__year=next_month.year)
        return queryset

class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'profissional', 'servico', 'data', 'hora', 'status')

    # Filtros no admin
    list_filter = (
        'status', 
        'profissional', 
        'servico',
        'data',  # Filtro por data
        DiaAgendamentoFilter,  # Filtro por dia
        SemanaAgendamentoFilter,  # Filtro por semana
        MesAgendamentoFilter,  # Filtro por mês
    )
    
    # Navegação por data
    date_hierarchy = 'data'

admin.site.register(Agendamento, AgendamentoAdmin)
