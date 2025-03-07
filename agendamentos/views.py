
# Create your views here.
from rest_framework import viewsets
from .models import Usuario, Profissional, Servico, Agendamento
from .serializers import UsuarioSerializer, ProfissionalSerializer, ServicoSerializer, AgendamentoSerializer

# ViewSet para o modelo Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# ViewSet para o modelo Profissional
class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

# ViewSet para o modelo Servico
class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

# ViewSet para o modelo Agendamento
class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
