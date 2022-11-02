from . import views

urlpatterns = [
    "comanda/",
    views.ComandaCriarView.as_view(),
    "comanda/comanda_id/produto/produto_id/",
    views.ComandaEditarApagarProdutoView.as_view(),
    "comanda/comanda_id/status/",
    views.ComandaEdicaoStatus.as_view(),
    "comanda/finalizadas/",
    views.ComandaListarComandasFinalizadas.as_view(),
    "comanda/abertas/",
    views.ComandaListarComandasAbertas.as_view(),
    "comanda/user/",
    views.ComandaListarTodasAsComandas.as_view(),
    "comanda/comanda_id/",
    views.ComandaEspecifica.as_view(),
]
