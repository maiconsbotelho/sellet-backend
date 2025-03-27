from rest_framework import serializers
from django.utils import timezone
from .models import Agendamento
from datetime import datetime

class AgendamentoSerializer(serializers.ModelSerializer):
    data_hora_agendamento = serializers.DateTimeField(required=False, read_only=True)

    class Meta:
        model = Agendamento
        fields = '__all__'

    def validate(self, data):
        """
        Valida os campos data e hora do agendamento:
        - Verifica se a data e hora do agendamento são no futuro.
        - Verifica se o horário já está ocupado para o mesmo profissional.
        - Verifica se o horário já está ocupado para o cliente (caso o usuário seja cliente).
        """
        # Combine data e hora para formar o `data_hora_agendamento`
        data_hora_agendamento = timezone.make_aware(datetime.combine(data['data'], data['hora']))

        # Verifica se o agendamento está no futuro
        if data_hora_agendamento <= timezone.now():
            raise serializers.ValidationError("A data e hora do agendamento devem ser no futuro.")

        # Obtém o profissional (usuário que está fazendo o agendamento)
        profissional = self.context['request'].user
        
        # Verifica se o horário já está ocupado para o mesmo profissional
        if Agendamento.objects.filter(profissional=profissional, data_hora_agendamento=data_hora_agendamento).exists():
            raise serializers.ValidationError("Esse horário já está ocupado para o profissional. Escolha outro horário.")
        
        # Verifica se o horário já está ocupado para o cliente, apenas se for um cliente
        if profissional.tipo_usuario == 'cliente':
            if Agendamento.objects.filter(cliente=profissional, data_hora_agendamento=data_hora_agendamento).exists():
                raise serializers.ValidationError("Esse horário já está ocupado para o cliente. Escolha outro horário.")
        
        # Retorna os dados validados para o próximo passo
        data['data_hora_agendamento'] = data_hora_agendamento
        return data

    def create(self, validated_data):
        """
        Durante a criação, o campo `data_hora_agendamento` já está gerado durante a validação.
        """
        return super().create(validated_data)
