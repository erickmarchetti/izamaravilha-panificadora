from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("login/", obtain_auth_token, name="user-login"),
    path("usuario/", views.CriarContasClientView.as_view(), name="user-create-client"),
    path(
        "funcionario/",
        views.CriarContasFuncionarioView.as_view(),
        name="user-create-employee",
    ),
    path(
        "usuario/contas/",
        views.ListarTodasContasApenasAdminView.as_view(),
        name="user-list-clients",
    ),
    path(
        "usuario/<str:usuario_id>/",
        views.ListarDeletarPropriaContaApenasAdminOuProprioView.as_view(),
        name="user-list-delete-self-client",
    ),
    path(
        "usuario/<str:usuario_id>/atualizar/",
        views.AtualizarPropriaContaView.as_view(),
        name="user-update-self-client",
    ),
]
