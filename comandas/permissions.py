from rest_framework.permissions import BasePermission

from comandas.models import Comanda_Produto


class ApenasDonoDaComanda(BasePermission):
    def has_object_permission(self, request, view, obj: Comanda_Produto):
        return request.user == obj.comanda.conta and obj.comanda.status == "aberta"
