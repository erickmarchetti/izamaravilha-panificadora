from rest_framework import serializers

from .models import Endereco
from .exceptions import ContaJaPossuiEnderecoCadastrado


class EnderecoDetalhadoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Endereco
        fields = [
            "id",
            "conta",
            "rua",
            "numero",
            "complemento",
            "cidade",
            "estado",
            "ponto_de_referencia",
        ]

    def create(self, validated_data):
        return Endereco.objects.create(**validated_data)


class EnderecoResumidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = [
            "rua",
            "numero",
            "complemento",
            "cidade",
            "estado",
            "ponto_de_referencia",
        ]

    def create(self, validated_data):
        conta = validated_data["conta"]

        if not Endereco.objects.filter(conta_id=conta.id):
            return Endereco.objects.create(**validated_data)

        raise ContaJaPossuiEnderecoCadastrado()
