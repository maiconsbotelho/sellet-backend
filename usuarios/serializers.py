from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import UserProfile
from core.services.usuario_service import adicionar_informacoes_ao_token

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return adicionar_informacoes_ao_token(token, user)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'telefone', 'foto_perfil', 'tipo_usuario', 'data_nascimento', 'endereco']