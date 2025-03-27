from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Servico
from .serializers import ServicoSerializer
from usuarios.permissions import IsProfissionalOrAdmin, IsAdmin


class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

    def perform_create(self, serializer):
        """
        Permite que apenas profissionais, administradores e superusuários criem serviços.
        - Profissionais: O serviço é vinculado automaticamente ao usuário autenticado.
        - Administradores e superusuários: Devem fornecer o profissional ao criar um serviço.
        """
        user = self.request.user

        if user.is_superuser or user.tipo_usuario == 'administrador':
            # Admins e superusuários podem criar serviços e devem informar o profissional
            serializer.save()
        elif user.tipo_usuario == 'profissional':
            # Profissionais criam serviços vinculados automaticamente a eles
            serializer.save(profissional=user)
        else:
            raise PermissionDenied("Apenas administradores e profissionais podem criar serviços.")

    def get_queryset(self):
        """
        Define o conjunto de serviços que cada tipo de usuário pode ver.
        """
        user = self.request.user
        if user.is_superuser or user.tipo_usuario == 'administrador':
            return Servico.objects.all()  # Admins veem todos os serviços

        if user.tipo_usuario == 'profissional':
            return Servico.objects.filter(profissional=user)  # Profissionais veem apenas os próprios serviços

        return Servico.objects.all()  # Clientes veem todos os serviços disponíveis
