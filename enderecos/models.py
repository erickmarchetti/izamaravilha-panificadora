from django.db import models
import uuid


class Endereco(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    cidade = models.TextField()
    estado = models.TextField()
    rua = models.TextField()
    numero = models.TextField()
    complemento = models.TextField()
    ponto_de_referencia = models.TextField()

    conta = models.OneToOneField(
        "contas.Conta",
        on_delete=models.CASCADE,
        related_name="endereco",
    )
