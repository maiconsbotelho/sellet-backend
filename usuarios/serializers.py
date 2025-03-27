from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import UserProfile

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adicione informações extras ao token
        token['email'] = user.email
        token['tipo_usuario'] = user.tipo_usuario
        token['username'] = user.username  # Inclua o username, se necessário
        return token

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'telefone', 'foto_perfil', 'tipo_usuario', 'data_nascimento', 'endereco']