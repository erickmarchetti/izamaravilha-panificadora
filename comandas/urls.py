from django.urls import path
from . import views


urlpatterns = [
    path("comanda/", views.ComandaAdicionarProdutoView.as_view()),
    path(
        "comanda/<comanda_id>/produto/<produto_id>/",
        views.ComandaEditarApagarProdutoView.as_view(),
    ),
    path("comanda/<comanda_id>/status/", views.ComandaEdicaoStatus.as_view()),
    path("comanda/finalizadas/", views.ComandaListarComandasFinalizadas.as_view()),
    path("comanda/abertas/", views.ComandaListarComandasAbertas.as_view()),
    path("comanda/user/", views.ComandaListarTodasAsComandas.as_view()),
    path("comanda/<comanda_id>/", views.ComandaEspecifica.as_view()),
]
