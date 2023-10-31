from rest_framework import serializers
from clientes.models import Cliente
from clientes.validators import *

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = '__all__'

    def validate(self, data):
    
        # Validar NOME
        if not validate_nome(data['nome']):
            raise serializers.ValidationError({'nome':"O nome precisa ser composto apenas por letras."})
        
        # Validar CPF
        if not validate_cpf(data['cpf']):
            raise serializers.ValidationError({'cpf':"Número de CPF inválido."})

        # Validar RG
        if not validate_rg(data['rg']):
            raise serializers.ValidationError({'rg':"O RG precisa ter 9 dígitos."})
        
        # Validar celular
        if not validate_celular(data['celular']):
            raise serializers.ValidationError({'celular':"O celular precisa ter exatamente este modelo: 11 12345-1234, respeitando o espaço e o traço."})

        return data