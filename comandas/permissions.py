from rest_framework.permissions import BasePermission

from comandas.models import Comanda_Produto


class ApenasDonoDaComanda(BasePermission):
    def has_object_permission(self, request, view, obj: Comanda_Produto):
        return request.user == obj.comanda.conta and obj.comanda.status == "aberta"


class ApenasDonoDaComandaListagem(BasePermission):
    def has_object_permission(self, request, view, obj: Comanda_Produto):
        return request.user == obj.conta


class ApenasAdministradorFuncionarioOuDonoDaComanda(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return (
            request.user == obj.conta
            or request.user.is_employee
            or request.user.is_superuser
        )


class ApenasAdministradorOuFuncionario(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.is_employee or request.user.is_superuser
