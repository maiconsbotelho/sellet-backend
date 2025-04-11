from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Agendamento
from .serializers import AgendamentoSerializer
from usuarios.permissions import IsProfissionalOrAdmin
from core.services.agendamento_service import associar_cliente_profissional, verificar_disponibilidade, validar_agendamento, pode_cancelar_agendamento


 


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]  # Exige que o usuário esteja autenticado

    def perform_create(self, serializer):
        """
        Ao criar um agendamento:
        - Valida a data e hora do agendamento.
        - Associa cliente e profissional com base no tipo de usuário.
        """
        user = self.request.user
        cliente_id = self.request.data.get('cliente')
        profissional_id = self.request.data.get('profissional')
        data = self.request.data.get('data')
        hora = self.request.data.get('hora')

        try:
            # Valida a data e hora do agendamento usando o método de classe do modelo
            data_hora_agendamento = validar_agendamento(
                data, hora, profissional_id, cliente_id
            )

            # Associa cliente e profissional ao agendamento
            associar_cliente_profissional(serializer, user, cliente_id, profissional_id)

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        if not pode_cancelar_agendamento(instance):
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