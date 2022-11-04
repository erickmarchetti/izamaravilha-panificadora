from django.db import models
import uuid

# Create your models here.
class Produto(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    categoria = models.ForeignKey(
        "categorias.Categoria", on_delete=models.CASCADE, related_name="produtos"
    )
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    nome = models.CharField(max_length=100)
    imagem = models.TextField()
    descricao = models.TextField(null=True)
