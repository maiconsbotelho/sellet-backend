from django.contrib import admin

from .models import Usuario, Profissional, Servico, Agendamento

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'telefone', 'manicure')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('manicure',)

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'avaliacao', 'quantidade_avaliacoes', 'cpf')
    search_fields = ('nome', 'cpf')
    list_filter = ('avaliacao',)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'qtde_slots')
    search_fields = ('nome',)
    list_filter = ('preco',)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'profissional', 'data')
    search_fields = ('usuario__nome', 'profissional__nome')
    list_filter = ('data',)
