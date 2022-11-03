from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Endereco
from .serializers import EnderecoDetalhadoSerializer, EnderecoResumidoSerializer
from .mixins import SerializerByMethodMixin
from .permissions import VerificarAutenticacao


class EnderecoView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [VerificarAutenticacao]

    queryset = Endereco.objects.all()
    serializer_map = {
        "GET": EnderecoDetalhadoSerializer,
        "POST": EnderecoResumidoSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(conta=self.request.user)


class EnderecoPorIDView(SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Endereco.objects.all()
    serializer_map = {
        "GET": EnderecoDetalhadoSerializer,
        "PATCH": EnderecoDetalhadoSerializer,
    }
