
# Create your views here.
from rest_framework import viewsets
from .models import Profissional
from .serializers import ProfissionalSerializer




# ViewSet para o modelo Profissional
class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

