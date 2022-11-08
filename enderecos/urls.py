from django.urls import path
from . import views

urlpatterns = [
    path(
        "endereco/",
        views.EnderecoPorIDView.as_view(),
    ),
]
