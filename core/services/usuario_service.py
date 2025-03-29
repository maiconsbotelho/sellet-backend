# filepath: /home/maicon/workspace/sellet/sellet-backend/core/services/usuario_service.py
from usuarios.models import UserProfile
from usuarios.permissions import IsAdmin, IsProfissional, IsCliente
from rest_framework.permissions import IsAuthenticated
from core.utils.helpers import (
    verificar_usuario_admin,
    verificar_usuario_profissional,
    verificar_usuario_cliente,
    verificar_usuario_profissional_ou_admin,
)
from rest_framework.exceptions import PermissionDenied

def obter_permissoes_usuario(request, action):
    if request.user.is_superuser:
        return []

    if action == 'list':
        return [IsAdmin()]
    elif action == 'retrieve':
        return [IsAuthenticated()]
    elif action in ['update', 'partial_update']:
        if verificar_usuario_admin(request.user):
            return [IsAdmin()]
        elif verificar_usuario_profissional(request.user):
            return [IsProfissional()]
        elif verificar_usuario_cliente(request.user):
            return [IsCliente()]
    elif action == 'create':
        return [IsAdmin()]
    elif action == 'destroy':
        return [IsAdmin()]
    return []

def obter_queryset_usuario(user):
    if not user.is_authenticated:
        # Se o usuário não estiver autenticado, você pode lançar uma exceção ou retornar um queryset vazio
        raise PermissionDenied("Você não está autenticado.")
    
    if user.is_superuser:
        return UserProfile.objects.all()
    if user.tipo_usuario == 'admin':
        return UserProfile.objects.all()
    return UserProfile.objects.filter(id=user.id)



    


def adicionar_informacoes_ao_token(token, user):
    token['email'] = user.email
    token['tipo_usuario'] = user.tipo_usuario
    token['username'] = user.username
    return token


# filepath: /home/maicon/workspace/sellet/sellet-backend/core/services/usuario_service.py
def verificar_usuario_admin(user):
    if not user.is_authenticated:  # Verifica se o usuário está autenticado
        return False
    return user.is_superuser or user.tipo_usuario == 'administrador'

def verificar_usuario_profissional(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.tipo_usuario == 'profissional'

def verificar_usuario_cliente(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.tipo_usuario == 'cliente'

def verificar_usuario_profissional_ou_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.tipo_usuario in ['profissional', 'administrador']