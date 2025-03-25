# usuarios/admin.py
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'tipo_usuario', 'email', 'telefone', 'data_nascimento', 'endereco', 'is_active')
    search_fields = ('username', 'email', 'tipo_usuario')
    list_filter = ('tipo_usuario', 'is_active')
