from django.db import models


class ComandaStatus(models.TextChoices):
    ABERTA = "aberta"
    FECHADA = "fechada"
    EM_ROTA_DE_ENTREGA = "em rota de entrega"
    ENTREGUE = "entregue"


class Comanda(models.Model):
    status = models.CharField(
        max_length=30, choices=ComandaStatus, default=ComandaStatus.ABERTA
    )
    data_criacao = models.DateField(auto_now_add=True)

    conta = models.ForeignKey(
        "contas.Conta", on_delete=models.CASCADE, references="comandas"
    )


class ComandaProduto(models.Model):
    quantidade = models.PositiveIntegerField()

    comanda = models.ForeignKey(
        "comandas.Comanda", on_delete=models.CASCADE, references="comanda_produtos"
    )
    produto = models.ForeignKey(
        "produtos.Produto", on_delete=models.CASCADE, references="comanda_produtos"
    )
