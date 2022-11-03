from rest_framework import generics
from produtos.models import Produto
from produtos.permissions import VendedorOuAdminPermissions
from rest_framework.authentication import TokenAuthentication
from produtos.serializers import ProdutoSerializer

# Create your views here.


class PatchDeleteProductView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [VendedorOuAdminPermissions]
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    # def perform_create(self, serializer):
    #     serializer.save(employee=self.request.user)


# nao precisa mais post separado!!!! testar a permissao do GetCreateAllProductsView
# class PostProductView(generics.CreateAPIView):
#     queryset = Produto.objects.all()
#     serializer_class = ProdutoSerializer

#     # def perform_create(self, serializer):
#     #     serializer.save(employee=self.request.user)


class GetCreateAllProductsView(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [VendedorOuAdminPermissions]
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class GetOnlyProducts(generics.RetrieveAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class GetOnlyProductsCategory(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        categoria_id = self.kwargs["categoria_id"]
        return self.queryset.filter(categoria_id=categoria_id)


class PegarProdutosRecemAtualizados(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        num = self.kwargs["atualizado_em"]
        return self.queryset.order_by("atualizado_em")[0:num]
