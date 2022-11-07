from rest_framework import serializers
from produtos.serializers import SerializerCategoriaProduto
from produtos.models import Produto
from .models import Estoque


class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = ["id", "quantidade", "atualizado_em"]
        read_only_fields = ["id", "atualizado_em"]


class AtualizarEstoqueSerializer(serializers.ModelSerializer):
    estoque = EstoqueSerializer(read_only=True)
    categoria = SerializerCategoriaProduto(read_only=True)
    quantidade = serializers.IntegerField(write_only=True)

    class Meta:
        model = Produto
        fields = [
            "id",
            "categoria",
            "preco",
            "nome",
            "imagem",
            "descricao",
            "estoque",
            "quantidade",
        ]

        read_only_fields = [
            "id",
            "categoria",
            "preco",
            "nome",
            "imagem",
            "descricao",
            "estoque",
        ]

    def update(self, instance, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance.estoque, key, value)
        instance.estoque.save()
        return instance
