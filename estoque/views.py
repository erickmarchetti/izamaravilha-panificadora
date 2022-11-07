from urllib import request
from rest_framework import generics
from .models import Estoque
from estoque.serializers import EstoqueSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .permissions import PermissaoAtualizarOuListarEstoqueAdmOuEmpregado


class AtualizaQuantidadeApenasAdmOuFunc(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser | PermissaoAtualizarOuListarEstoqueAdmOuEmpregado]
    serializer_class = EstoqueSerializer
    queryset = Estoque.objects.all()


class PegaDoEstoqueQtdPositiva(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser | PermissaoAtualizarOuListarEstoqueAdmOuEmpregado]
    serializer_class = EstoqueSerializer
    queryset = Estoque.objects.all()

    def get_queryset(self):
        filtradoQuantidadePositivo = self.request.query_params.get("quantidade", 0)
        return Estoque.objects.filter(quantidade__lte=filtradoQuantidadePositivo)
