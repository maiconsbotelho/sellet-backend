from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Agendamento
from .serializers import AgendamentoSerializer
from .permissions import IsProfissionalOrAdmin

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]  # Exige que o usuário esteja autenticado

    def perform_create(self, serializer):
        """
        Ao criar um agendamento, associamos o cliente ou profissional ao agendamento.
        """
        user = self.request.user
        if user.tipo_usuario == 'cliente':
            serializer.save(cliente=user)
        elif user.tipo_usuario == 'profissional':
            serializer.save(profissional=user)

    def get_permissions(self):
        """
        Profissionais e administradores podem acessar todos os agendamentos,
        enquanto clientes podem acessar apenas seus próprios agendamentos.
        """
        if self.action in ['list', 'retrieve']:
            return [IsProfissionalOrAdmin()]
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
        Modifica o queryset para permitir que um cliente veja apenas seus próprios agendamentos.
        Profissionais e administradores podem ver todos os agendamentos.
        """
        user = self.request.user
        if user.tipo_usuario == 'cliente':
            return Agendamento.objects.filter(cliente=user)
        elif user.tipo_usuario == 'profissional':
            return Agendamento.objects.filter(profissional=user)
        return Agendamento.objects.all()
