# filepath: /home/maicon/workspace/sellet/sellet-backend/usuarios/test_usuarios.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

class UserProfileTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()

        # Criando os usuários com emails únicos
        self.admin_user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            tipo_usuario='administrador'
        )
        self.profissional_user = get_user_model().objects.create_user(
            username='profissional',
            email='profissional@example.com',
            password='profissional123',
            tipo_usuario='profissional'
        )
        self.cliente_user = get_user_model().objects.create_user(
            username='cliente',
            email='cliente@example.com',
            password='cliente123',
            tipo_usuario='cliente'
        )

        # Logs para depuração
        print("Admin ID:", self.admin_user.id)
        print("Profissional ID:", self.profissional_user.id)
        print("Cliente ID:", self.cliente_user.id)

        # Verifica se os usuários foram criados
        self.assertTrue(get_user_model().objects.filter(username='admin').exists())
        self.assertTrue(get_user_model().objects.filter(username='profissional').exists())
        self.assertTrue(get_user_model().objects.filter(username='cliente').exists())

        # URLs para os testes
        self.admin_url = reverse('userprofile-list')
        self.user_profile_url = reverse('userprofile-detail', args=[self.cliente_user.id])
        print("User Profile URL:", self.user_profile_url)

    def test_criar_usuario_admin(self):
        """Testa se um administrador pode criar um novo usuário"""
        self.client.force_authenticate(user=self.admin_user)  # Autentica o administrador
        response = self.client.post(self.admin_url, {
            'username': 'novo_cliente',
            'email': 'novo_cliente@example.com',
            'password': 'senha123',
            'tipo_usuario': 'cliente'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tipo_usuario'], 'cliente')

    def test_criar_usuario_sem_permissao(self):
        """Testa se um profissional ou cliente não pode criar um usuário"""
        for user in [self.profissional_user, self.cliente_user]:
            self.client.force_authenticate(user=user)  # Autentica o usuário
            response = self.client.post(self.admin_url, {
                'username': 'novo_usuario',
                'email': 'novo_usuario@example.com',
                'password': 'senha123',
                'tipo_usuario': 'cliente'
            })
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listar_usuarios_admin(self):
        """Testa se um administrador pode listar todos os usuários"""
        self.client.force_authenticate(user=self.admin_user)  # Autentica o administrador
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('admin', str(response.data))
        self.assertIn('cliente', str(response.data))  # Verifica se o cliente está na resposta

    def test_listar_usuarios_sem_permissao(self):
        """Testa se um usuário não administrador não pode listar usuários"""
        for user in [self.profissional_user, self.cliente_user]:
            self.client.force_authenticate(user=user)  # Autentica o usuário
            response = self.client.get(self.admin_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_visualizar_perfil_usuario(self):
        """Testa se um usuário pode visualizar seu próprio perfil"""
        self.client.force_authenticate(user=self.cliente_user)  # Autentica o cliente
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'cliente')

 

    def test_editar_perfil_usuario(self):
        """Testa se um usuário pode editar seu próprio perfil"""
        self.client.force_authenticate(user=self.cliente_user)  # Autentica o cliente
        response = self.client.patch(self.user_profile_url, {'telefone': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['telefone'], '1234567890')

    

    def test_deletar_usuario_admin(self):
        """Testa se um administrador pode excluir um usuário"""
        self.client.force_authenticate(user=self.admin_user)  # Autentica o administrador
        # Verifica se o cliente existe antes de deletar
        self.assertTrue(get_user_model().objects.filter(id=self.cliente_user.id).exists())
        response = self.client.delete(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   

    