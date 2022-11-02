from rest_framework import generics

from contas.models import Conta
from .serializers import ContaClienteSerializer, ContaFuncionarioSerializer, RecuperarDadosContaCompletaClienteFuncionarioSerializer, AtualizarPropriaContaSerializer
from rest_framework.authentication import TokenAuthentication
from .permissions import ContaDeAdministradorAuthToken, ContaPropriaAuthToken, ContaPropriaOuAdministradorAuthToken
from utils.mixins import SerializerByMethodMixin
from django.contrib.auth.hashers import make_password
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


class ListarDeletarPropriaContaApenasAdminOuProprioView(SerializerByMethodMixin, generics.RetrieveDestroyAPIView):

    queryset = Conta.objects.all()
    serializer_map = {
        'GET': ContaClienteSerializer,
        'DELETE': RecuperarDadosContaCompletaClienteFuncionarioSerializer
    }

    lookup_url_kwarg = 'usuario_id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [ContaPropriaOuAdministradorAuthToken]


class AtualizarPropriaContaView(generics.UpdateAPIView):

    queryset = Conta.objects.all()
    serializer_class = AtualizarPropriaContaSerializer
    lookup_url_kwarg = 'usuario_id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [ContaPropriaAuthToken]


    def perform_update(self, serializer):

        dados_da_conta = self.request.data  

        senha_hasheada = make_password(dados_da_conta['password'])

        serializer.save(password=senha_hasheada) 


        
        






        









    





