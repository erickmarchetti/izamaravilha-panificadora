from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from comandas.models import Comanda, Comanda_Produto, ComandaStatus
from comandas.serializers import (
    AdicionarOuListarProdutoSerializer,
    EditarProdutoSerializer,
    EditarQuantidadeProdutoSerializer,
    ListarProdutoSerializer,
)
from comandas.permissions import (
    ApenasAdministradorFuncionarioOuDonoDaComanda,
    ApenasAdministradorOuFuncionario,
    ApenasDonoDaComanda,
)


class ComandaAdicionarProdutoView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Comanda.objects.all()
    serializer_class = AdicionarOuListarProdutoSerializer

    def perform_create(self, serializer):
        serializer.save(conta=self.request.user)


class ComandaEditarApagarProdutoView(generics.UpdateAPIView, generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ApenasDonoDaComanda]

    queryset = Comanda.objects.all()
    serializer_class = EditarQuantidadeProdutoSerializer

    def get_object(self):
        comanda_id = self.kwargs["comanda_id"]
        produto_id = self.kwargs["produto_id"]

        comanda_produto = get_object_or_404(
            Comanda_Produto, comanda_id=comanda_id, produto_id=produto_id
        )

        self.check_object_permissions(self.request, comanda_produto)

        return comanda_produto


class ComandaEdicaoStatus(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ApenasAdministradorFuncionarioOuDonoDaComanda]

    queryset = Comanda.objects.all()
    serializer_class = EditarProdutoSerializer
    lookup_url_kwarg = "comanda_id"

    def perform_update(self, serializer):
        return serializer.save(conta=self.request.user)


class ComandaListarComandasFinalizadas(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ApenasAdministradorOuFuncionario]

    queryset = Comanda.objects.all()
    serializer_class = ListarProdutoSerializer

    def get_queryset(self):
        return self.queryset.filter(status=ComandaStatus.FECHADA)


class ComandaListarComandasAbertas(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ApenasAdministradorOuFuncionario]

    queryset = Comanda.objects.all()
    serializer_class = ListarProdutoSerializer

    def get_queryset(self):
        return self.queryset.filter(status=ComandaStatus.ABERTA)


class ComandaListarTodasAsComandas(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ApenasDonoDaComanda]

    queryset = Comanda.objects.all()
    serializer_class = AdicionarOuListarProdutoSerializer

    def get_queryset(self):
        return self.request.user.comandas.all()


class ComandaEspecifica(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ApenasDonoDaComanda]

    queryset = Comanda.objects.all()
    serializer_class = ListarProdutoSerializer
    lookup_url_kwarg = "comanda_id"
