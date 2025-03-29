# filepath: /home/maicon/workspace/sellet/sellet-backend/usuarios/permissions.py
from rest_framework.permissions import BasePermission
from core.utils.helpers import (
    verificar_usuario_admin,
    verificar_usuario_profissional,
    verificar_usuario_cliente,
    verificar_usuario_profissional_ou_admin,
)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and verificar_usuario_admin(request.user)

class IsProfissional(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and verificar_usuario_profissional(request.user)

class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and verificar_usuario_cliente(request.user)

class IsProfissionalOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and verificar_usuario_profissional_ou_admin(request.user)