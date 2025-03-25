from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from .permissions import IsAdmin, IsProfissional, IsCliente

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        """
        Define as permissões para as ações baseadas no tipo de usuário.
        """
        if self.action == 'list':  # Visualizar todos os usuários
            return [IsAdmin()]
        
        elif self.action == 'retrieve':  # Visualizar um usuário específico
            return [IsAuthenticated()]  # Qualquer usuário autenticado pode visualizar seu próprio perfil

        elif self.action in ['update', 'partial_update']:  # Editar um usuário
            if self.request.user.tipo_usuario == 'administrador':
                return [IsAdmin()]
            elif self.request.user.tipo_usuario == 'profissional':
                return [IsProfissional()]
            elif self.request.user.tipo_usuario == 'cliente':
                return [IsCliente()]

        elif self.action == 'create':  # Criar um usuário
            return [IsAdmin()]  # Somente administradores podem criar usuários

        elif self.action == 'destroy':  # Deletar um usuário
            return [IsAdmin()]  # Somente administradores podem deletar clientes ou profissionais

        return super().get_permissions()

    def get_queryset(self):
        """
        Ajusta o queryset baseado no tipo de usuário autenticado.
        Administradores veem todos os usuários, enquanto profissionais e clientes
        veem apenas seus próprios perfis.
        """
        user = self.request.user
        if user.tipo_usuario == 'admin':
            return UserProfile.objects.all()  # Administradores podem ver todos os usuários
        return UserProfile.objects.filter(id=user.id)  # Profissionais e clientes veem apenas seus próprios perfis
