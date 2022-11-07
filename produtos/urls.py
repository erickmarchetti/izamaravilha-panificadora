from django.urls import path
from .views import (
    PatchDeleteProductView,
    GetCreateAllProductsView,
    GetOnlyProductsCategory,
    PegarProdutosRecemAtualizados,
)

urlpatterns = [
    path("produtos/", GetCreateAllProductsView.as_view()),
    path("produtos/categoria/<pk>/", GetOnlyProductsCategory.as_view()),
    path("produtos/recentes/", PegarProdutosRecemAtualizados.as_view()),
    path("produtos/<pk>/", PatchDeleteProductView.as_view()),
]
