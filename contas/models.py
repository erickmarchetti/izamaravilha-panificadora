from django.contrib.auth.models import AbstractUser
from django.db import models


class Conta(AbstractUser):

    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=120)
    is_employee = models.BooleanField(default=False)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15)
    pontos_de_fidelidade = models.IntegerField(default=0)

    # endereco = models.OneToOneField('enderecos.Endereco', on_delete=models.CASCADE, related_name='conta')



    REQUIRED_FIELDS = ['first_name', 'last_name', 'data_nascimento', 'cpf', 'telefone',]