from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Endereco
from .serializers import EnderecoDetalhadoSerializer


class EnderecoPorIDView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Endereco.objects.all()
    serializer_class = EnderecoDetalhadoSerializer

    def get_object(self):
        return self.request.user.endereco
