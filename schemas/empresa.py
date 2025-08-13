from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime

from ..validators import validar_cnpj, CNPJError

class EmpresaBase(BaseModel):
    """Schema base para Empresa, contendo campos comuns para criação e atualização."""
    nome: str = Field(..., min_length=3, max_length=255, description="Nome da empresa")
    cnpj: str = Field(..., description="CNPJ da empresa (apenas números ou formatado)")
    endereco: str = Field(..., min_length=5, max_length=600, description="Endereço completo da empresa")
    email: EmailStr = Field(..., description="E-mail de contato da empresa")
    telefone: str = Field(..., min_length=10, max_length=15, description="Telefone de contato da empresa")

    @validator('cnpj')
    def cnpj_must_be_valid(cls, v):
        """Valida se o CNPJ é válido."""
        if not validar_cnpj(v):
            raise ValueError('CNPJ inválido')
        # Retorna o CNPJ apenas com números
        return ''.join(filter(str.isdigit, v))

    class Config:
        schema_extra = {
            "example": {
                "nome": "Empresa Exemplo Ltda",
                "cnpj": "12345678000100",
                "endereco": "Rua Exemplo, 123, Centro, Cidade - Estado",
                "email": "contato@empresaexemplo.com.br",
                "telefone": "11999998888"
            }
        }

class EmpresaCreate(EmpresaBase):
    """Schema para criação de uma nova empresa."""
    pass

class EmpresaUpdate(BaseModel):
    """Schema para atualização de uma empresa existente."""
    nome: Optional[str] = Field(None, min_length=3, max_length=255, description="Nome da empresa")
    cnpj: Optional[str] = Field(None, description="CNPJ da empresa (apenas números ou formatado)")
    endereco: Optional[str] = Field(None, min_length=5, max_length=600, description="Endereço completo da empresa")
    email: Optional[EmailStr] = Field(None, description="E-mail de contato da empresa")
    telefone: Optional[str] = Field(None, min_length=10, max_length=15, description="Telefone de contato da empresa")

    @validator('cnpj')
    def cnpj_must_be_valid(cls, v):
        """Valida se o CNPJ é válido (quando fornecido)."""
        if v is not None and not validar_cnpj(v):
            raise ValueError('CNPJ inválido')
        return v if v is None else ''.join(filter(str.isdigit, v))

    class Config:
        schema_extra = {
            "example": {
                "nome": "Novo Nome da Empresa",
                "endereco": "Novo Endereço, 456, Centro, Cidade - Estado",
                "email": "novoemail@empresa.com.br",
                "telefone": "11988887777"
            }
        }

class EmpresaInDBBase(EmpresaBase):
    """Schema base para leitura de uma empresa do banco de dados."""
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True

class Empresa(EmpresaInDBBase):
    """Schema para retorno de uma empresa."""
    pass
