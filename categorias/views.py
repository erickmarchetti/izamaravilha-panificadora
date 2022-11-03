from rest_framework import generics
from .models import Categoria
from categorias.serializer import SerializerCategoria
from rest_framework.authentication import TokenAuthentication
from .permissoesCategoria import PermissaoCriarCategoria, PermissaoAtualizarCategoria


class CategoriasListarOuCriar(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PermissaoCriarCategoria]

    serializer_class = SerializerCategoria
    queryset = Categoria.objects.all()


class CategoriasPegarOuAtualizar(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PermissaoAtualizarCategoria]
    serializer_class = SerializerCategoria
    queryset = Categoria.objects.all()