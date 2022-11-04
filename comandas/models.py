from django.db import models
import uuid


class ComandaStatus(models.TextChoices):
    ABERTA = "aberta"
    FECHADA = "fechada"
    EM_ROTA_DE_ENTREGA = "em rota de entrega"
    ENTREGUE = "entregue"


class Comanda(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.CharField(
        max_length=30, choices=ComandaStatus.choices, default=ComandaStatus.ABERTA
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    conta = models.ForeignKey(
        "contas.Conta", on_delete=models.CASCADE, related_name="comandas"
    )


class Comanda_Produto(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    quantidade = models.PositiveIntegerField()

    comanda = models.ForeignKey(
        "comandas.Comanda", on_delete=models.CASCADE, related_name="comanda_produto"
    )
    produto = models.ForeignKey(
        "produtos.Produto", on_delete=models.CASCADE, related_name="comanda_produto"
    )
