from rest_framework.permissions import BasePermission
from rest_framework.views import Request


class VerificarAutenticacao(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method == "POST" or (
            request.user.is_authenticated
            and (request.user.is_employee or request.user.is_superuser)
        )


class ContaPropriaAuthToken(BasePermission):
    def has_object_permission(self, request, view, obj):
        usuario_id = request.user.id
        obj_id = obj.id

        return request.user.is_authenticated and usuario_id == obj_id
