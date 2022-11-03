from rest_framework.views import Request
from rest_framework.permissions import BasePermission


class PermissaoCriarCategoria(BasePermission):
    def has_permission(self, request: Request, view):
        return (
            request.method == "GET"
            or request.user.is_employee
            or request.user.is_superuser
        )


class PermissaoAtualizarCategoria(BasePermission):
    def has_object_permission(self, request, view, categorias):
        return (
            request.method == "GET"
            or request.user.is_employee
            or request.user.is_superuser
        )
