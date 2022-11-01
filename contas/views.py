from django.shortcuts import render
from rest_framework import generics

from contas.models import Conta
from .serializers import ContaClienteSerializer, ContaFuncionarioSerializer

# Create your views here.

class CriarContasClientView(generics.CreateAPIView):

    queryset = Conta.objects.all()
    serializer_class = ContaClienteSerializer


class CriarContasFuncionarioView(generics.CreateAPIView):

    queryset = Conta.objects.all()
    serializer_class = ContaFuncionarioSerializer
