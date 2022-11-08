from django.db import models
import uuid


class Categoria(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nome = models.CharField(max_length=20, unique=True)
    # fk 1 to n com produtos Sendo categoria como lado 1
