from rest_framework import generics
from categorias.models import Categoria
from categorias.serializers import SerializerCategoria
from produtos.models import Produto
from produtos.permissions import VendedorOuAdminPermissions
from rest_framework.authentication import TokenAuthentication
from produtos.serializers import ProdutoSerializer
import ipdb

# Create your views here.


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
        # ipdb.set_trace()
        return self.queryset.filter(categoria_id=categoria_id)
        # CATEGORIA RETIORNA MAS NOA CONSIGO CRIAR MAIS UM PRODUTO COM A MESMA CATEGORIA


class PegarProdutosRecemAtualizados(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        num = self.kwargs["atualizado_em"]
        return self.queryset.order_by("atualizado_em")[0:num]
