from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import UserProfile
from core.services.usuario_service import adicionar_informacoes_ao_token

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Verifique se o usuário está ativo
        if not user.is_active:
            raise serializers.ValidationError("Conta inativa. Entre em contato com o suporte.")

        # Inclua o tipo_usuario no token
        data['tipo_usuario'] = user.tipo_usuario
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id','username', 'first_name', 'last_name', 'email', 'password', 'cpf', 'telefone',
            'tipo_usuario', 'data_nascimento', 'foto_perfil', 'endereco',
            'cep', 'uf', 'cidade', 'bairro', 'rua', 'numero'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user
