from django.urls import path
from . import views

urlpatterns = [
    path("estoque/<produto_id>/", views.AtualizaQuantidadeApenasAdmOuFunc.as_view()),
    path("estoque/", views.PegaDoEstoqueQtdPositiva.as_view()),
]
