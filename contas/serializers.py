from rest_framework import serializers

from .models import Conta






class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    password = serializers.CharField()


class ContaClienteSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=256, write_only=True)


    class Meta:
        model = Conta
        fields = ['id', 'username','password', 'first_name', 'last_name', 'telefone', 'cpf', 'data_nascimento', 'is_employee', 'pontos_de_fidelidade',]
        read_only_fields = ['id', 'is_employee', 'pontos_de_fidelidade']

    
    def create(self, validated_data):
        
        return Conta.objects.create_user(**validated_data)


class ContaFuncionarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = Conta
        fields = ['id', 'username','password', 'first_name', 'last_name', 'telefone', 'cpf', 'data_nascimento', 'is_employee', 'pontos_de_fidelidade',]
        read_only_fields = ['id', 'is_employee', 'pontos_de_fidelidade']

    
    def create(self, validated_data):
        
        return Conta.objects.create_user(**validated_data, is_employee=True)

         