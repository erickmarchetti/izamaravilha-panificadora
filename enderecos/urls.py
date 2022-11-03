from django.urls import path
from . import views

urlpatterns = [
    path(
        "endereco/",
        views.EnderecoView.as_view(),
    ),
    path(
        "endereco/<pk>/",
        views.EnderecoPorIDView.as_view(),
    ),
]
