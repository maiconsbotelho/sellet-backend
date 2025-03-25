from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Agendamento, Servico

class RelatorioTests(APITestCase):

    def setUp(self):
        # Criando um usuário administrador
        self.admin_user = get_user_model().objects.create_user(
            username='admin', password='admin123', tipo_usuario='administrador'
        )
        # Criando um profissional
        self.profissional_user = get_user_model().objects.create_user(
            username='profissional', password='profissional123', tipo_usuario='profissional'
        )
        # Criando agendamentos e serviços para o teste
        self.servico_1 = Servico.objects.create(
            nome="Serviço A", descricao="Descrição do serviço A", valor=100.00, duracao=30, profissional=self.profissional_user
        )
        self.agendamento_1 = Agendamento.objects.create(
            cliente=self.admin_user,
            profissional=self.profissional_user,
            servico=self.servico_1,
            data_hora_agendamento="2025-04-01 10:00:00",
            status="confirmado"
        )
        
        self.client.login(username='admin', password='admin123')

    def test_relatorio_agendamentos(self):
        response = self.client.get('/api/relatorio/agendamentos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('agendamentos_por_profissional', response.data)

    def test_relatorio_servicos(self):
        response = self.client.get('/api/relatorio/servicos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('servicos_populares', response.data)
