from rest_framework import serializers
from .models import Servico



class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'  # Inclui todos os campos do modelo Servico