from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Agendamento
from .serializers import AgendamentoSerializer
from usuarios.permissions import IsProfissionalOrAdmin


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]  # Exige que o usuário esteja autenticado

    def perform_create(self, serializer):
        """
        Ao criar um agendamento:
        - Clientes são vinculados automaticamente ao agendamento.
        - Profissionais são vinculados automaticamente ao agendamento.
        - Administradores e superusuários precisam fornecer cliente e profissional manualmente.
        """
        user = self.request.user

        # Administradores e superusuários fornecem manualmente cliente e profissional
        if user.is_superuser or user.tipo_usuario == 'administrador':
            cliente = self.request.data.get('cliente')
            profissional = self.request.data.get('profissional')
            
            if not cliente or not profissional:
                return Response(
                    {"detail": "Administrador deve fornecer cliente e profissional."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(cliente_id=cliente, profissional_id=profissional)
        
        elif user.tipo_usuario == 'cliente':
            serializer.save(cliente=user)
        
        elif user.tipo_usuario == 'profissional':
            serializer.save(profissional=user)
        
        else:
            return Response(
                {"detail": "Apenas administradores, profissionais e clientes podem criar agendamentos."},
                status=status.HTTP_403_FORBIDDEN
            )

    def get_permissions(self):
        """
        Profissionais e administradores podem acessar todos os agendamentos,
        enquanto clientes podem acessar apenas seus próprios agendamentos.
        """
        if self.action in ['list', 'retrieve']:
            return [IsProfissionalOrAdmin()]  # Admins e profissionais podem listar/ver detalhes
        return super().get_permissions()

    def perform_destroy(self, instance):
        """
        Valida se o agendamento pode ser cancelado.
        O cancelamento só pode ser feito até 24h antes do agendamento.
        """
        if not instance.pode_ser_cancelado():
            return Response(
                {"detail": "O cancelamento só pode ser feito até 24h antes do agendamento."},
                status=status.HTTP_400_BAD_REQUEST
            )
        super().perform_destroy(instance)

    def get_queryset(self):
        """
        Modifica o queryset para:
        - Clientes veem apenas seus próprios agendamentos.
        - Profissionais veem apenas seus próprios agendamentos.
        - Administradores e superusuários veem todos os agendamentos.
        """
        user = self.request.user
        if user.is_superuser or user.tipo_usuario == 'administrador':
            return Agendamento.objects.all()
        elif user.tipo_usuario == 'cliente':
            return Agendamento.objects.filter(cliente=user)
        elif user.tipo_usuario == 'profissional':
            return Agendamento.objects.filter(profissional=user)
        return Agendamento.objects.none()  # Outros usuários não devem acessar agendamentos
