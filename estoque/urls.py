from django.urls import path
from . import views

urlpatterns = [
    path("estoque/", views.AtualizaQuantidadeApenasAdmOuFunc.as_view()),
    path("estoque/<pk>/", views.PegaDoEstoqueQtdPositiva.as_view()),
]
