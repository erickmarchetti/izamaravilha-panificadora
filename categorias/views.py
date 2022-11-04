from rest_framework import generics
from .models import Categoria
from categorias.serializers import SerializerCategoria


class CategoriasListarOuCriar(generics.ListCreateAPIView):
    serializer_class = SerializerCategoria
    queryset = Categoria.objects.all()


class CategoriasPegarOuAtualizar(generics.RetrieveUpdateAPIView):
    serializer_class = SerializerCategoria
    queryset = Categoria.objects.all()
