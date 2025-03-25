from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserProfileTests(APITestCase):
    
    def setUp(self):
        # Criando os usuários
        self.admin_user = get_user_model().objects.create_user(
            username='admin', password='admin123', tipo_usuario='administrador'
        )
        self.profissional_user = get_user_model().objects.create_user(
            username='profissional', password='profissional123', tipo_usuario='profissional'
        )
        self.cliente_user = get_user_model().objects.create_user(
            username='cliente', password='cliente123', tipo_usuario='cliente'
        )
        
        # URLs para os testes
        self.admin_url = reverse('userprofile-list')
        self.user_profile_url = reverse('userprofile-detail', args=[self.cliente_user.id])

    def test_criar_usuario_admin(self):
        """Testa se um administrador pode criar um novo usuário"""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(self.admin_url, {
            'username': 'novo_cliente',
            'password': 'senha123',
            'tipo_usuario': 'cliente'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tipo_usuario'], 'cliente')

    def test_criar_usuario_sem_permissao(self):
        """Testa se um profissional ou cliente não pode criar um usuário"""
        self.client.login(username='profissional', password='profissional123')
        response = self.client.post(self.admin_url, {
            'username': 'novo_profissional',
            'password': 'senha123',
            'tipo_usuario': 'profissional'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listar_usuarios_admin(self):
        """Testa se um administrador pode listar todos os usuários"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('admin', str(response.data))
        self.assertIn('cliente', str(response.data))

    def test_listar_usuarios_sem_permissao(self):
        """Testa se um usuário não administrador não pode listar usuários"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_visualizar_perfil_usuario(self):
        """Testa se um usuário pode visualizar seu próprio perfil"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'cliente')

    def test_editar_perfil_usuario(self):
        """Testa se um usuário pode editar seu próprio perfil"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.patch(self.user_profile_url, {'telefone': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['telefone'], '1234567890')

    def test_editar_perfil_outro_usuario(self):
        """Testa se um usuário não pode editar o perfil de outro usuário"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.patch(reverse('userprofile-detail', args=[self.profissional_user.id]), {'telefone': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deletar_usuario_admin(self):
        """Testa se um administrador pode excluir um usuário"""
        self.client.login(username='admin', password='admin123')
        response = self.client.delete(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deletar_usuario_sem_permissao(self):
        """Testa se um usuário não administrador não pode excluir outro usuário"""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.delete(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
