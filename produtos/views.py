from rest_framework import generics
from categorias.models import Categoria
from categorias.serializers import SerializerCategoria
from produtos.models import Produto
from produtos.permissions import VendedorOuAdminPermissions
from rest_framework.authentication import TokenAuthentication
from produtos.serializers import ProdutoSerializer
import ipdb
from django.shortcuts import get_object_or_404


class PatchDeleteProductView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [VendedorOuAdminPermissions]
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class GetCreateAllProductsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [VendedorOuAdminPermissions]
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class GetOnlyProducts(generics.RetrieveAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class GetOnlyProductsCategory(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        categoria_id = self.kwargs["pk"]

        return self.queryset.filter(categoria_id=categoria_id)


def get_object_by_id(model, **kwargs):
    obj = get_object_or_404(model, kwargs)
    return obj


class PegarProdutosRecemAtualizados(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


# def get_queryset(self):
#     produto_id = self.kwargs["id"]
#     produto = get_object_by_id(Produto, id=produto_id)
#     estoque = Estoque.objects.filter(produtos=produto)
#     return estoque
#     # num = self.kwargs["atualizado_em"]
#     # return self.queryset.order_by("atualizado_em")[0:num]
