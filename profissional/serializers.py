from rest_framework import serializers
from .models import Profissional





class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = '__all__'  # Inclui todos os campos do modelo Profissional