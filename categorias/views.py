from rest_framework import generics
from .models import Categoria

from categorias.serializer import SerializerCategoria
from rest_framework.authentication import TokenAuthentication
from .permissions import PermissaoLerOuApenasFuncionario



class CategoriasListarOuCriar(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PermissaoLerOuApenasFuncionario]

    serializer_class = SerializerCategoria
    queryset = Categoria.objects.all()


class CategoriasPegarOuAtualizar(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PermissaoLerOuApenasFuncionario]
    serializer_class = SerializerCategoria
    queryset = Categoria.objects.all()
