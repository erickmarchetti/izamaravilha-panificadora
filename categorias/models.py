from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=20, unique=True)
    # fk 1 to n com produtos Sendo categoria como lado 1
