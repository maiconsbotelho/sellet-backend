from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Servico
from .serializers import ServicoSerializer
from .permissions import IsProfissionalOrAdmin  # Permissões específicas para profissionais e administradores

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [IsAuthenticated]  # Exige que o usuário esteja autenticado
    
    def perform_create(self, serializer):
        """
        Vincula o profissional automaticamente ao criar o serviço.
        Garante que apenas profissionais possam criar um serviço.
        """
        if self.request.user.tipo_usuario == 'profissional':
            serializer.save(profissional=self.request.user)
        else:
            raise PermissionDenied("Você não tem permissão para criar serviços.")

    def get_permissions(self):
        """
        Administradores têm permissão total para criar, editar, listar e excluir serviços.
        Profissionais podem criar e editar seus próprios serviços.
        Clientes não podem criar ou editar serviços.
        """
        if self.request.user.tipo_usuario == 'admin':
            # Administradores têm permissões totais
            return [IsAuthenticated()]
        if self.action in ['list', 'retrieve']:
            # Profissionais e administradores podem acessar os serviços
            return [IsProfissionalOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Modifica o queryset dependendo do tipo de usuário:
        - Administradores podem ver todos os serviços.
        - Profissionais podem ver apenas seus próprios serviços.
        - Clientes podem ver todos os serviços (ou, caso precise, apenas serviços públicos).
        """
        user = self.request.user
        if user.tipo_usuario == 'admin':
            return Servico.objects.all()  # Administradores podem ver todos os serviços
        elif user.tipo_usuario == 'profissional':
            return Servico.objects.filter(profissional=user)  # Profissionais veem apenas seus serviços
        return Servico.objects.all()  # Clientes podem ver todos os serviços, ou você pode limitar isso se desejar
