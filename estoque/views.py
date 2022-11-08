from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from estoque.serializers import AtualizarEstoqueSerializer, EstoqueSerializer
from .models import Estoque
from .permissions import PermissaoAtualizarOuListarEstoqueAdmOuEmpregado

from produtos.models import Produto

from drf_spectacular.utils import extend_schema


class AtualizaQuantidadeApenasAdmOuFunc(generics.UpdateAPIView):
    lookup_url_kwarg = "produto_id"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser | PermissaoAtualizarOuListarEstoqueAdmOuEmpregado]
    serializer_class = AtualizarEstoqueSerializer
    queryset = Produto.objects.all()

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


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
