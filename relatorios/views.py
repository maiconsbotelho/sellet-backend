from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import datetime
from .models import Agendamento, Servico
from django.db.models import Count

class RelatorioAgendamentosView(APIView):
    permission_classes = [IsAdminUser]  # Apenas administradores podem acessar

    def get(self, request):
        # Exemplo de relatório de agendamentos com contagem por profissional
        agendamentos = Agendamento.objects.values('profissional__username') \
            .annotate(total_agendamentos=Count('id')) \
            .order_by('-total_agendamentos')

        data = {
            "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "agendamentos_por_profissional": list(agendamentos),
        }

        return Response(data)


class RelatorioServicosView(APIView):
    permission_classes = [IsAdminUser]  # Apenas administradores podem acessar

    def get(self, request):
        # Exemplo de relatório de serviços com total de agendamentos
        servicos = Servico.objects.values('nome') \
            .annotate(total_agendamentos=Count('agendamento')) \
            .order_by('-total_agendamentos')

        data = {
            "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "servicos_populares": list(servicos),
        }

        return Response(data)

