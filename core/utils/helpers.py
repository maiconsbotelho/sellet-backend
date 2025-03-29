# filepath: /home/maicon/workspace/sellet/sellet-backend/core/utils/verificacoes_usuario.py

def verificar_usuario_admin(user):
    return user.is_superuser or user.tipo_usuario == 'administrador'

def verificar_usuario_profissional(user):
    return user.is_superuser or user.tipo_usuario == 'profissional'

def verificar_usuario_cliente(user):
    return user.is_superuser or user.tipo_usuario == 'cliente'

def verificar_usuario_profissional_ou_admin(user):
    return user.is_superuser or user.tipo_usuario in ['profissional', 'administrador']