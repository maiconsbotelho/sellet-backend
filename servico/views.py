
# Create your views here.
from rest_framework import viewsets
from .models import Servico
from .serializers import ServicoSerializer



# ViewSet para o modelo Servico
class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

