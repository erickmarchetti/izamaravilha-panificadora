from django.db import models
import uuid

class Estoque(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    quantidade = models.IntegerField()
    atualizado_em = models.DateTimeField(auto_now=True)