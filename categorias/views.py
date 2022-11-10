from rest_framework import generics
from .models import Categoria

from categorias.serializers import SerializerCategoria
from rest_framework.authentication import TokenAuthentication
from .permissions import PermissaoLerOuApenasFuncionario

from drf_spectacular.utils import extend_schema


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

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
