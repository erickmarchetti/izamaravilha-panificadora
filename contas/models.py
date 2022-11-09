import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from cpf_field.models import CPFField

from django.utils.crypto import get_random_string


class Conta(AbstractUser):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=120)
    is_employee = models.BooleanField(default=False)
    data_nascimento = models.DateField()
    cpf = CPFField("cpf", unique=True)
    telefone = models.CharField(max_length=15)
    pontos_de_fidelidade = models.IntegerField(default=0)
    secret_key = models.CharField(
        max_length=6, default=get_random_string(6, "0123456789"), editable=False
    )

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "data_nascimento",
        "cpf",
        "telefone",
    ]
