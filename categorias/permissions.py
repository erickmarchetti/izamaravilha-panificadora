from rest_framework.views import Request
from rest_framework.permissions import BasePermission


class PermissaoLerOuApenasFuncionario(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method == "GET" or (
            request.user.is_authenticated
            and (request.user.is_employee or request.user.is_superuser)
        )
