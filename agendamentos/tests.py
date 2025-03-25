from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from .models import Agendamento
from django.urls import reverse

class AgendamentoTests(APITestCase):
    def setUp(self):
        # Criando um administrador
        self.admin_user = get_user_model().objects.create_user(
            username='admin', password='admin123', tipo_usuario='administrador'
        )
        self.profissional_user = get_user_model().objects.create_user(
            username='profissional', password='profissional123', tipo_usuario='profissional'
        )
        self.cliente_user = get_user_model().objects.create_user(
            username='cliente', password='cliente123', tipo_usuario='cliente'
        )

        self.client.login(username='admin', password='admin123')

    def test_agendamento_para_o_futuro(self):
        """Testa se um agendamento pode ser feito apenas para o futuro"""
        futuro = timezone.now() + timedelta(hours=1)
        response = self.client.post(reverse('agendamento-list'), {
            'data_hora_agendamento': futuro,
            'profissional': self.profissional_user.id,
            'cliente': self.cliente_user.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Agendamento no passado
        passado = timezone.now() - timedelta(hours=1)
        response = self.client.post(reverse('agendamento-list'), {
            'data_hora_agendamento': passado,
            'profissional': self.profissional_user.id,
            'cliente': self.cliente_user.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A data e hora do agendamento devem ser no futuro.', str(response.data))

    def test_horario_ja_ocupado(self):
        """Testa se o horário do profissional está sendo verificado"""
        futuro = timezone.now() + timedelta(hours=1)
        agendamento_existente = Agendamento.objects.create(
            data_hora_agendamento=futuro,
            profissional=self.profissional_user,
            cliente=self.cliente_user,
        )

        # Tentando criar outro agendamento no mesmo horário
        response = self.client.post(reverse('agendamento-list'), {
            'data_hora_agendamento': futuro,
            'profissional': self.profissional_user.id,
            'cliente': self.cliente_user.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Esse horário já está ocupado. Escolha outro horário.', str(response.data))

    def test_associar_cliente_ao_agendamento(self):
        """Testa se o cliente está sendo associado corretamente ao agendamento"""
        futuro = timezone.now() + timedelta(hours=1)
        response = self.client.post(reverse('agendamento-list'), {
            'data_hora_agendamento': futuro,
            'profissional': self.profissional_user.id,
            'cliente': self.cliente_user.id,
        })
        agendamento = Agendamento.objects.first()
        self.assertEqual(agendamento.cliente, self.cliente_user)

    def test_cancelamento_ate_24h_antes(self):
        """Testa se o cancelamento só pode ocorrer até 24h antes do agendamento"""
        futuro = timezone.now() + timedelta(hours=1)
        agendamento = Agendamento.objects.create(
            data_hora_agendamento=futuro,
            profissional=self.profissional_user,
            cliente=self.cliente_user,
        )
        
        response = self.client.delete(reverse('agendamento-detail', args=[agendamento.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Criando um agendamento para testar cancelamento com menos de 24h
        passado_24h = timezone.now() + timedelta(minutes=30)
        agendamento = Agendamento.objects.create(
            data_hora_agendamento=passado_24h,
            profissional=self.profissional_user,
            cliente=self.cliente_user,
        )

        response = self.client.delete(reverse('agendamento-detail', args=[agendamento.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('O cancelamento só pode ser feito até 24h antes do agendamento.', str(response.data))

    def test_acesso_permissao_agendamento(self):
        """Testa as permissões de acesso aos agendamentos"""
        # Cliente não pode ver agendamentos de outros clientes
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(reverse('agendamento-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Cliente não tem agendamentos ainda
        
        # Profissional pode ver seus próprios agendamentos
        self.client.login(username='profissional', password='profissional123')
        response = self.client.get(reverse('agendamento-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admin pode ver todos os agendamentos
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('agendamento-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
