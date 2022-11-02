from rest_framework import generics
from .models import Estoque
from estoque.serializer import EstoqueSerializer
from rest_framework.authentication import TokenAuthentication


class AtualizaQuantidadeApenasAdmOuFunc(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    serializer_class = [EstoqueSerializer]
    queryset = Estoque.objects.all()


class PegaDoEstoqueQtdPositiva(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    serializer_class = [EstoqueSerializer]
    queryset = Estoque.objects.all()
