from urllib import request
from rest_framework import generics
from .models import Estoque
from estoque.serializers import AtualizarEstoqueSerializer, EstoqueSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .permissions import PermissaoAtualizarOuListarEstoqueAdmOuEmpregado
from produtos.models import Produto


class AtualizaQuantidadeApenasAdmOuFunc(generics.UpdateAPIView):
    lookup_url_kwarg = "produto_id"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser | PermissaoAtualizarOuListarEstoqueAdmOuEmpregado]
    serializer_class = AtualizarEstoqueSerializer
    queryset = Produto.objects.all()


class PegaDoEstoqueQtdPositiva(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser | PermissaoAtualizarOuListarEstoqueAdmOuEmpregado]
    serializer_class = AtualizarEstoqueSerializer
    queryset = Produto.objects.all()

    def get_queryset(self):
        filtradoQuantidadePositivo = self.request.query_params.get("quantidade", 0)
        return [
            estoque.produto
            for estoque in Estoque.objects.filter(
                quantidade__lte=filtradoQuantidadePositivo
            )
        ]
