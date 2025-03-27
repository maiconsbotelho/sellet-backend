from rest_framework import serializers
from .models import Servico
from usuarios.models import UserProfile

class ServicoSerializer(serializers.ModelSerializer):
    profissionais = serializers.PrimaryKeyRelatedField(
        many=True,  # Indica que é uma relação de muitos para muitos
        queryset=UserProfile.objects.filter(tipo_usuario='profissional')  # Apenas profissionais
    )

    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'duracao', 'preco', 'profissionais']