from rest_framework import permissions


class ContaDeAdministradorAuthToken(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.is_authenticated and request.user.is_superuser


class ContaPropriaAuthToken(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        usuario_id = request.user.id
        obj_id = obj.id

        return request.user.is_authenticated and usuario_id == obj_id


class ContaPropriaOuAdministradorAuthToken(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        usuario_id = request.user.id
        obj_id = obj.id

        return (
            request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_authenticated
            and usuario_id == obj_id
        )
