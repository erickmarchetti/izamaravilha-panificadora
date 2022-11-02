from django.shortcuts import get_object_or_404
from rest_framework import generics
from comandas.models import Comanda, Comanda_Produto, ComandaStatus

from comandas.serializers import ComandaProdutoSerializer, ComandaSerializer


class ComandaCriarView(generics.CreateAPIView):
    queryset = Comanda.objects
    serializer_class = ComandaSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class ComandaEditarApagarProdutoView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comanda.objects.all()
    serializer_class = Comanda

    def get_object(self):
        comanda_id = self.kwargs["comanda_id"]
        produto_id = self.kwargs["produto_id"]

        return get_object_or_404(
            Comanda_Produto, comanda_id=comanda_id, produto_id=produto_id
        )


class ComandaEdicaoStatus(generics.UpdateAPIView):
    queryset = Comanda.objects.all()
    serializer_class = ComandaSerializer
    lookup_url_kwarg = "comanda_id"


class ComandaListarComandasFinalizadas(generics.ListAPIView):
    queryset = Comanda.objects.all()
    serializer_class = ComandaSerializer

    def get_queryset(self):
        return self.queryset.filter(status=ComandaStatus.FECHADA)


class ComandaListarComandasAbertas(generics.ListAPIView):
    queryset = Comanda.objects.all()
    serializer_class = ComandaSerializer

    def get_queryset(self):
        return self.queryset.filter(status=ComandaStatus.ABERTA)


class ComandaListarTodasAsComandas(generics.ListAPIView):
    queryset = Comanda.objects.all()
    serializer_class = ComandaSerializer


class ComandaEspecifica(generics.RetrieveAPIView):
    queryset = Comanda.objects.all()
    serializer_class = ComandaSerializer
    lookup_url_kwarg = "comanda_id"
