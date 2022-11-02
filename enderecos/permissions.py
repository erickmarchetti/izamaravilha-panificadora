from rest_framework.permissions import BasePermission
from rest_framework.views import Request


class VerificarAutenticacao(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method == "POST" or (
            request.user.is_authenticated
            and (request.user.is_employee or request.user.is_superuser)
        )
