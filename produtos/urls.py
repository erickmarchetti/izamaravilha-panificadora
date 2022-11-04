from django.urls import path
from .views import (
    PatchDeleteProductView,
    GetCreateAllProductsView,
    GetOnlyProducts,
    GetOnlyProductsCategory,
)

urlpatterns = [
    path("produtos/<pk>/", PatchDeleteProductView.as_view()),
    path("produtos/", GetCreateAllProductsView.as_view()),
    path("produtos/<pk>/", GetOnlyProducts.as_view()),
    path("produtos/categoria/<pk>/", GetOnlyProductsCategory.as_view()),
]
