from rest_framework import serializers
from django.utils import timezone
from .models import Agendamento
from datetime import datetime
from .models import Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    data_hora_agendamento = serializers.DateTimeField(required=False, read_only=True)

    class Meta:
        model = Agendamento
        fields = '__all__'

    def validate(self, data):
        """
        Valida os campos data e hora do agendamento usando o método de classe do modelo.
        """
        profissional = self.context['request'].user
        cliente = data.get('cliente', None) if profissional.tipo_usuario == 'administrador' else profissional

        # Use o método de classe do modelo para validar o agendamento
        data_hora_agendamento = Agendamento.validar_agendamento(
            data['data'], data['hora'], profissional, cliente
        )
        data['data_hora_agendamento'] = data_hora_agendamento
        return data

    def create(self, validated_data):
        """
        Durante a criação, o campo `data_hora_agendamento` já está gerado durante a validação.
        """
        return super().create(validated_data)
