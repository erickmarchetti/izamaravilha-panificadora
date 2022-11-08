from rest_framework import serializers

from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404

from comandas.models import Comanda, Comanda_Produto
from contas.models import Conta
from produtos.models import Produto

from utils.services import (
    pegar_ou_criar_comanda_mais_nova,
    verificar_se_produto_tem_estoque,
    listar_produtos_de_uma_comanda,
    verificar_status_comanda,
    verificar_produtos_comanda,
)


class AdicionarOuListarProdutoSerializer(serializers.ModelSerializer):
    produto_id = serializers.UUIDField(
        write_only=True,
    )
    quantidade = serializers.IntegerField(
        write_only=True, validators=[MinValueValidator(1)]
    )
    produtos = serializers.SerializerMethodField(method_name="listar_produtos")

    class Meta:
        model = Comanda
        fields = [
            "id",
            "status",
            "data_criacao",
            "conta",
            "produto_id",
            "quantidade",
            "produtos",
        ]
        read_only_fields = ["id", "status", "data_criacao", "conta"]

    def listar_produtos(self, comanda: Comanda):
        return listar_produtos_de_uma_comanda(comanda)

    def create(self, validated_data):

        dono_comanda: Conta = validated_data["conta"]

        produto = get_object_or_404(Produto, id=validated_data["produto_id"])

        verificar_se_produto_tem_estoque(produto, validated_data["quantidade"])

        comanda_mais_nova = pegar_ou_criar_comanda_mais_nova(dono_comanda)

        verificar_produtos_comanda(comanda_mais_nova, produto)

        comanda_mais_nova.comanda_produto.create(
            produto=produto,
            quantidade=validated_data["quantidade"],
        )

        return comanda_mais_nova


class EditarQuantidadeProdutoSerializer(serializers.ModelSerializer):
    quantidade = serializers.IntegerField(
        write_only=True, validators=[MinValueValidator(1)]
    )
    produtos = serializers.SerializerMethodField(method_name="listar_produtos")

    class Meta:
        model = Comanda
        fields = [
            "id",
            "status",
            "data_criacao",
            "conta",
            "quantidade",
            "produtos",
        ]
        read_only_fields = ["id", "status", "data_criacao", "conta"]

    def listar_produtos(self, comanda: Comanda):
        return listar_produtos_de_uma_comanda(comanda)

    def update(self, instance: Comanda_Produto, validated_data: dict):

        verificar_se_produto_tem_estoque(instance.produto, validated_data["quantidade"])

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance.comanda


class EditarStatusComandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comanda
        fields = [
            "id",
            "status",
            "data_criacao",
            "conta",
        ]
        read_only_fields = [
            "id",
            "data_criacao",
            "conta",
        ]

    def update(self, instance, validated_data: dict):

        dono_escolhas = ["fechada"]
        funcionario_escolhas = ["em rota de entrega", "entregue"]

        verificar_status_comanda(
            instance,
            validated_data,
            dono_escolhas,
            funcionario_escolhas,
        )

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
