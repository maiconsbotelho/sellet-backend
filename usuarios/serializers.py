# usuarios/serializers.py
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'telefone', 'foto_perfil', 'tipo_usuario', 'data_nascimento', 'endereco']
