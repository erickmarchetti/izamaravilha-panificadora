from rest_framework import serializers
from enderecos.serializers import EnderecoResumidoSerializer
from enderecos.models import Endereco

from .models import Conta
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    password = serializers.CharField()


class ContaClienteSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=256, write_only=True)
    endereco = EnderecoResumidoSerializer()

    class Meta:
        model = Conta
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
            "endereco",
        ]
        read_only_fields = ["id", "is_employee", "pontos_de_fidelidade",]

    def create(self, validated_data):

        dados_endereco = validated_data.pop('endereco')

        usuario = Conta.objects.create_user(**validated_data)

        Endereco.objects.create(**dados_endereco, conta=usuario)

        return usuario


class ContaFuncionarioSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=256, write_only=True)
    endereco = EnderecoResumidoSerializer()

    class Meta:
        model = Conta
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
            "endereco"
        ]
        read_only_fields = ["id", "is_employee", "pontos_de_fidelidade"]

    def create(self, validated_data):
        
        dados_endereco = validated_data.pop('endereco')

        usuario = Conta.objects.create_user(**validated_data, is_employee=True)

        Endereco.objects.create(**dados_endereco, conta=usuario)

        return usuario


class RecuperarDadosContaCompletaClienteFuncionarioSerializer(
    serializers.ModelSerializer
):

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = Conta
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
        ]
        read_only_fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
        ]


class AtualizarPropriaContaSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = Conta
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
        ]
        read_only_fields = [
            "id",
            "cpf",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
        ]

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            if key == "password":
                valor_alterado = make_password(value)
            else:
                valor_alterado = value

            setattr(instance, key, valor_alterado)

        instance.save()

        return instance
