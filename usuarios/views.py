from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from .permissions import IsAdmin, IsProfissional, IsCliente
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from core.services.usuario_service import obter_permissoes_usuario, obter_queryset_usuario



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        return obter_permissoes_usuario(self.request, self.action)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.tipo_usuario == 'administrador':
            return UserProfile.objects.all()
        return UserProfile.objects.filter(id=user.id)