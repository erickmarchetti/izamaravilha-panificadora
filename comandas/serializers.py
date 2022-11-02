from rest_framework import serializers
from django.core.validators import MinValueValidator
from comandas.models import Comanda, Comanda_Produto


class ComandaProdutoSerializer(serializers.ModelSerializer):
    preco = serializers.SerializerMethodField()

    class Meta:
        model = Comanda_Produto
        fields = ["id", "quantidade", "comanda", "produto"]
        read_only_fields = ["id"]


class ComandaSerializer(serializers.ModelSerializer):
    produto_id = serializers.UUIDField(write_only=True)
    quantidade = serializers.IntegerField(
        write_only=True, validators=[MinValueValidator(1)]
    )
    produtos = serializers.SerializerMethodField(method_name="listar_produtos")

    class Meta:
        model = Comanda
        fields = ["id", "status", "data_criacao", "conta", "quantidade", "produto_id"]
        read_only_fields = ["id", "status", "data_criacao", "conta"]

    def listar_produtos(self, obj):
        self.validated_data
