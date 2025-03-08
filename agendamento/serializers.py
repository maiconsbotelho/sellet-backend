from rest_framework import serializers
from .models import Agendamento
from servico.models import Servico



class AgendamentoSerializer(serializers.ModelSerializer):
    servicos = serializers.PrimaryKeyRelatedField(many=True, queryset=Servico.objects.all())

    class Meta:
        model = Agendamento
        fields = ['id', 'data', 'status', 'created_at', 'updated_at', 'cliente', 'profissional', 'servicos']
