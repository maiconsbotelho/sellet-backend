from rest_framework import serializers
from django.utils import timezone
from .models import Agendamento
from datetime import datetime
from core.services.agendamento_service import (
    verificar_disponibilidade,
    validar_agendamento,
    associar_cliente_profissional
) 

class AgendamentoSerializer(serializers.ModelSerializer):
    data_hora_agendamento = serializers.DateTimeField(required=False, read_only=True)

    class Meta:
        model = Agendamento
        fields = '__all__'


    def validate(self, data):
        # Verifica se o horário está disponível
        profissional = data.get("profissional")
        data_agendamento = data.get("data")
        hora_agendamento = data.get("hora")

        if Agendamento.objects.filter(profissional=profissional, data=data_agendamento, hora=hora_agendamento).exists():
            raise serializers.ValidationError("O horário selecionado não está disponível.")
        return data


    def create(self, validated_data):
        """
        Durante a criação, o campo `data_hora_agendamento` já está gerado durante a validação.
        """
        return super().create(validated_data)
