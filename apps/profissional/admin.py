from django.contrib import admin
from .models import Profissional

# Register your models here.
@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)
    list_filter = ('nome',)