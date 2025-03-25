from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Servico

class ServicoTests(APITestCase):

    def setUp(self):
        # Criando usuários
        self.admin_user = get_user_model().objects.create_user(
            username='admin', password='admin123', tipo_usuario='administrador'
        )
        self.profissional_user = get_user_model().objects.create_user(
            username='profissional', password='profissional123', tipo_usuario='profissional'
        )
        self.cliente_user = get_user_model().objects.create_user(
            username='cliente', password='cliente123', tipo_usuario='cliente'
        )

        # Criando serviços
        self.servico_1 = Servico.objects.create(
            nome="Serviço A", descricao="Descrição do serviço A", valor=100.00, duracao=30, profissional=self.profissional_user
        )
        self.servico_2 = Servico.objects.create(
            nome="Serviço B", descricao="Descrição do serviço B", valor=200.00, duracao=60, profissional=self.profissional_user
        )

        # URLs para os testes
        self.servico_url = reverse('servico-list')
        self.servico_detail_url = reverse('servico-detail', args=[self.servico_1.id])

    def test_criar_servico_admin(self):
        """Testa se um administrador pode criar um novo serviço"""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(self.servico_url, {
            'nome': 'Novo Serviço',
            'descricao': 'Descrição do novo serviço',
            'valor': 150.00,
            'duracao': 45,
            'profissional': self.profissional_user.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'Novo Serviço')

    def test_criar_servico_profissional(self):
        """Testa se um profissional pode criar um serviço"""
        self.client.login(username='profissional', password='profissional123')
        response = self.client.post(self.servico_url, {
            'nome': 'Serviço do Profissional',
            'descricao': 'Descrição do serviço do profissional',
            'valor': 120.00,
            'duracao': 40,
            'profissional': self.profissional_user.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'Serviço do Profissional')

    def test_criar_servico_sem_permissao(self):
        """Testa se um cliente não pode criar um serviço"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.post(self.servico_url, {
            'nome': 'Serviço do Cliente',
            'descricao': 'Descrição do serviço do cliente',
            'valor': 90.00,
            'duracao': 30,
            'profissional': self.profissional_user.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listar_servicos_admin(self):
        """Testa se um administrador pode listar todos os serviços"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(self.servico_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Serviço A', str(response.data))
        self.assertIn('Serviço B', str(response.data))

    def test_listar_servicos_profissional(self):
        """Testa se um profissional pode listar os seus serviços"""
        self.client.login(username='profissional', password='profissional123')
        response = self.client.get(self.servico_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Serviço A', str(response.data))
        self.assertIn('Serviço B', str(response.data))

    def test_listar_servicos_cliente(self):
        """Testa se um cliente não pode listar os serviços"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(self.servico_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_visualizar_servico(self):
        """Testa se um usuário pode visualizar os detalhes de um serviço"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(self.servico_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Serviço A')

    def test_editar_servico_admin(self):
        """Testa se um administrador pode editar um serviço"""
        self.client.login(username='admin', password='admin123')
        response = self.client.patch(self.servico_detail_url, {'nome': 'Serviço A - Atualizado'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Serviço A - Atualizado')

    def test_editar_servico_profissional(self):
        """Testa se um profissional pode editar seus próprios serviços"""
        self.client.login(username='profissional', password='profissional123')
        response = self.client.patch(self.servico_detail_url, {'nome': 'Serviço A - Atualizado pelo Profissional'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Serviço A - Atualizado pelo Profissional')

    def test_editar_servico_cliente(self):
        """Testa se um cliente não pode editar um serviço"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.patch(self.servico_detail_url, {'nome': 'Serviço A - Atualizado pelo Cliente'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deletar_servico_admin(self):
        """Testa se um administrador pode excluir um serviço"""
        self.client.login(username='admin', password='admin123')
        response = self.client.delete(self.servico_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deletar_servico_profissional(self):
        """Testa se um profissional pode excluir seus próprios serviços"""
        self.client.login(username='profissional', password='profissional123')
        response = self.client.delete(self.servico_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deletar_servico_cliente(self):
        """Testa se um cliente não pode excluir um serviço"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.delete(self.servico_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
