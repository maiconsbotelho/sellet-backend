from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Servico
from .serializers import ServicoSerializer
from usuarios.permissions import IsProfissionalOrAdmin, IsAdmin

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [IsAuthenticated, IsProfissionalOrAdmin]

    def perform_create(self, serializer):
        """
        Permite que profissionais e administradores criem serviços.
        """
        user = self.request.user
        if user.is_superuser or user.tipo_usuario == 'administrador':
            # Admins podem criar serviços e associar profissionais
            serializer.save()
        elif user.tipo_usuario == 'profissional':
            # Profissionais criam serviços e se associam automaticamente
            servico = serializer.save()
            servico.profissionais.add(user)
        else:
            raise PermissionDenied("Você não tem permissão para criar serviços.")
        

    def get_queryset(self):
        """
        Define o conjunto de serviços que cada tipo de usuário pode ver.
        """
        user = self.request.user
        if user.is_superuser or user.tipo_usuario == 'administrador':
            # Admins veem todos os serviços
            return Servico.objects.all()

        if user.tipo_usuario == 'profissional':
            # Profissionais veem apenas os serviços aos quais estão associados
            return Servico.objects.filter(profissionais=user)

        # Clientes veem todos os serviços disponíveis
        return Servico.objects.all()