from django.urls import path
from . import views

urlpatterns = [
    path("categorias/", views.CategoriasListarOuCriar.as_view()),
    path("categorias/<pk/>", views.CategoriasPegarOuAtualizar.as_view()),
]
