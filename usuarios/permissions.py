# usuarios/permissions.py
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.tipo_usuario == 'administrador'

class IsProfissional(BasePermission):
    def has_permission(self, request, view):
        return request.user.tipo_usuario == 'profissional'

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            return obj == request.user
        return True

class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user.tipo_usuario == 'cliente'

    def has_object_permission(self, request, view, obj):
        return obj == request.user
    
class IsProfissionalOrAdmin(BasePermission):
    """
    Permite acesso apenas a usuários que são profissionais ou administradores.
    """

    def has_permission(self, request, view):
        return request.user.tipo_usuario in ['profissional', 'administrador']

