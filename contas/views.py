from rest_framework import generics

from contas.models import Conta
from .serializers import (
    ContaClienteSerializer,
    ContaFuncionarioSerializer,
    RecuperarDadosContaCompletaClienteFuncionarioSerializer,
    AtualizarPropriaContaSerializer,
    VerificarConta,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    ContaDeAdministradorAuthToken,
    ContaPropriaAuthToken,
    ContaPropriaOuAdministradorAuthToken,
)
from utils.mixins import SerializerByMethodMixin

# Create your views here.


class CriarContasClientView(generics.CreateAPIView):

    queryset = Conta.objects.all()
    serializer_class = ContaClienteSerializer


class CriarContasFuncionarioView(generics.CreateAPIView):

    queryset = Conta.objects.all()
    serializer_class = ContaFuncionarioSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [ContaDeAdministradorAuthToken]


class ListarTodasContasApenasAdminView(generics.ListAPIView):

    queryset = Conta.objects.all()
    serializer_class = ContaClienteSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [ContaDeAdministradorAuthToken]


class ListarContaPropriaView(generics.RetrieveAPIView):

    queryset = Conta.objects.all()
    serializer_class = ContaClienteSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):

        return self.request.user

class DeletarContaPropriaOuAdminView(generics.DestroyAPIView):

    queryset = Conta.objects.all()
    serializer_class = RecuperarDadosContaCompletaClienteFuncionarioSerializer
    lookup_url_kwarg = "usuario_id"

    authentication_classes = [TokenAuthentication]
    permission_classes = [ContaPropriaAuthToken]


class AtualizarPropriaContaView(generics.UpdateAPIView):

    queryset = Conta.objects.all()
    serializer_class = AtualizarPropriaContaSerializer
    lookup_url_kwarg = "usuario_id"

    authentication_classes = [TokenAuthentication]
    permission_classes = [ContaPropriaAuthToken]


class ValidarEmailView(generics.UpdateAPIView):

    queryset = Conta.objects.all()
    serializer_class = VerificarConta
    lookup_field = "secret_key"
    lookup_url_kwarg = "secret_key"

    def perform_update(self, serializer):

        serializer.save(secret_key=self.kwargs["secret_key"])
