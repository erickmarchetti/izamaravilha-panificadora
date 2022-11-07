from django.urls import path
from .views import (
    PatchDeleteProductView,
    GetCreateAllProductsView,
    GetOnlyProductsCategory,
)

urlpatterns = [
    path("produtos/<pk>/", PatchDeleteProductView.as_view()),
    path("produtos/", GetCreateAllProductsView.as_view()),
    path("produtos/categoria/<pk>/", GetOnlyProductsCategory.as_view()),
]
