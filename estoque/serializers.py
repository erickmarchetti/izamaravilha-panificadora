from rest_framework import serializers
from .models import Estoque


class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = ["id", "quantidade", "atualizado_em"]
        read_only_fields = ["id", "atualizado_em"]
