import re
from validate_docbr import CPF

def validate_cpf(numero_cpf):
    return CPF().validate(numero_cpf)

def validate_nome(nome):
    return nome.isalpha()

def validate_rg(rg):
    return len(rg) == 9

def validate_celular(celular):
    """Verifica se o número do celular é válido."""
    modelo = '[0-9]{2} [0-9]{5}-[0-9]{4}'
    resposta = re.findall(modelo, celular)
    return resposta