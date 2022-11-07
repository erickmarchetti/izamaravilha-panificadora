from django.db import models
from produtos.models import Produto
import uuid


class Estoque(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    quantidade = models.IntegerField()
    atualizado_em = models.DateTimeField(auto_now=True)
    produto = models.OneToOneField(
        Produto, on_delete=models.CASCADE, related_name="estoque"
    )
