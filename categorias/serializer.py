from rest_framework import serializers
from .models import Categoria


class SerializerCategoria(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome"]
        read_only_fields = ["id"]
