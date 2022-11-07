from rest_framework.permissions import BasePermission


class PermissaoAtualizarOuListarEstoqueAdmOuEmpregado(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method == "PATCH"
            or request.method == "GET"
            and request.user.is_authenticated()
            and request.user.is_superuser
            or request.user.is_employee
        )
