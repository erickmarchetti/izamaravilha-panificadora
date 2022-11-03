from django.urls import path
from .views import (
    PatchDeleteProductView,
    # PostProductView,
    GetCreateAllProductsView,
    GetOnlyProducts,
    GetOnlyProductsCategory,
)

urlpatterns = [
    # path("produtos/", PostProductView.as_view()),
    path("produtos/<pk>/", PatchDeleteProductView.as_view()),
    path("produtos/", GetCreateAllProductsView.as_view()),
    path("produtos/<pk>/", GetOnlyProducts.as_view()),
    path("produtos/<categoria_id>/", GetOnlyProductsCategory.as_view()),
]
