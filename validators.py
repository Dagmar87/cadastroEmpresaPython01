import re
from typing import Any, Optional

class CNPJError(ValueError):
    """Exceção para erros de validação de CNPJ."""
    pass

def validar_cnpj(cnpj: str) -> bool:
    """
    Valida um CNPJ.
    
    Args:
        cnpj: CNPJ a ser validado (com ou sem formatação)
        
    Returns:
        bool: True se o CNPJ for válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais
    if len(set(cnpj)) == 1:
        return False
    
    # Cálculo do primeiro dígito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso = 9 if peso == 2 else peso - 1
    
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj[12]) != digito1:
        return False
    
    # Cálculo do segundo dígito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso = 9 if peso == 2 else peso - 1
    
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    return int(cnpj[13]) == digito2

def formatar_cnpj(cnpj: str) -> str:
    """
    Formata um CNPJ no padrão 00.000.000/0000-00.
    
    Args:
        cnpj: CNPJ a ser formatado
        
    Returns:
        str: CNPJ formatado
        
    Raises:
        CNPJError: Se o CNPJ não for válido
    """
    if not validar_cnpj(cnpj):
        raise CNPJError("CNPJ inválido")
    
    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    # Formata o CNPJ (00.000.000/0000-00)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
