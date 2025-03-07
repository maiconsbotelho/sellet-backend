from rest_framework import serializers
from .models import Usuario
from .models import Profissional
from .models import Servico
from .models import Agendamento

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'  # Isto vai incluir todos os campos do modelo Usuario


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = '__all__'  # Inclui todos os campos do modelo Profissional


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'  # Inclui todos os campos do modelo Servico


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'  # Inclui todos os campos do modelo Agendamento