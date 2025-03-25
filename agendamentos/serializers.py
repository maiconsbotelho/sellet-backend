from rest_framework import serializers
from django.utils import timezone
from .models import Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'
    
    def validate_data_hora_agendamento(self, value):
        # Verifica se o agendamento está no futuro
        if value <= timezone.now():
            raise serializers.ValidationError("A data e hora do agendamento devem ser no futuro.")
        
        # Verifica se o horário já está ocupado para o mesmo profissional
        profissional = self.context['request'].user
        if Agendamento.objects.filter(profissional=profissional, data_hora_agendamento=value).exists():
            raise serializers.ValidationError("Esse horário já está ocupado. Escolha outro horário.")
        
        # Verifica se o horário já está ocupado para o cliente (apenas se for cliente)
        if profissional.tipo_usuario == 'cliente':
            if Agendamento.objects.filter(cliente=profissional, data_hora_agendamento=value).exists():
                raise serializers.ValidationError("Esse horário já está ocupado. Escolha outro horário.")
        
        return value
