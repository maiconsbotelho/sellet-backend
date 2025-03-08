
# Create your views here.
from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer


# ViewSet para o modelo Usuario
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

