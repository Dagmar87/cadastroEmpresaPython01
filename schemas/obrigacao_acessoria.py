from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Periodicidade(str, Enum):
    """Enum para os tipos de periodicidade de uma obrigação acessória."""
    DIARIA = "Diária"
    SEMANAL = "Semanal"
    QUINZENAL = "Quinzenal"
    MENSAL = "Mensal"
    BIMESTRAL = "Bimestral"
    TRIMESTRAL = "Trimestral"
    SEMESTRAL = "Semestral"
    ANUAL = "Anual"
    EVENTUAL = "Eventual"

class ObrigacaoAcessoriaBase(BaseModel):
    """Schema base para ObrigacaoAcessoria, contendo campos comuns para criação e atualização."""
    nome: str = Field(..., min_length=3, max_length=255, description="Nome da obrigação acessória")
    periodicidade: Periodicidade = Field(..., description="Periodicidade da obrigação")
    empresa_id: int = Field(..., gt=0, description="ID da empresa à qual a obrigação está vinculada")
    descricao: Optional[str] = Field(None, max_length=1000, description="Descrição detalhada da obrigação")
    data_vencimento: Optional[str] = Field(None, description="Data de vencimento no formato YYYY-MM-DD")

    @validator('data_vencimento')
    def validar_data_vencimento(cls, v):
        """Valida o formato da data de vencimento."""
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Formato de data inválido. Use YYYY-MM-DD')
        return v

    class Config:
        schema_extra = {
            "example": {
                "nome": "Declaração Mensal de Serviços",
                "periodicidade": "Mensal",
                "empresa_id": 1,
                "descricao": "Declaração mensal de serviços prestados",
                "data_vencimento": "2023-12-31"
            }
        }

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    """Schema para criação de uma nova obrigação acessória."""
    pass

class ObrigacaoAcessoriaUpdate(BaseModel):
    """Schema para atualização de uma obrigação acessória existente."""
    nome: Optional[str] = Field(None, min_length=3, max_length=255, description="Nome da obrigação acessória")
    periodicidade: Optional[Periodicidade] = Field(None, description="Periodicidade da obrigação")
    descricao: Optional[str] = Field(None, max_length=1000, description="Descrição detalhada da obrigação")
    data_vencimento: Optional[str] = Field(None, description="Data de vencimento no formato YYYY-MM-DD")
    
    @validator('data_vencimento')
    def validar_data_vencimento(cls, v):
        """Valida o formato da data de vencimento."""
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Formato de data inválido. Use YYYY-MM-DD')
        return v

    class Config:
        schema_extra = {
            "example": {
                "nome": "Declaração Anual de Serviços",
                "periodicidade": "Anual",
                "descricao": "Declaração anual de serviços prestados",
                "data_vencimento": "2023-12-31"
            }
        }

class ObrigacaoAcessoriaInDBBase(ObrigacaoAcessoriaBase):
    """Schema base para leitura de uma obrigação acessória do banco de dados."""
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True

class ObrigacaoAcessoria(ObrigacaoAcessoriaInDBBase):
    """Schema para retorno de uma obrigação acessória."""
    pass

class ObrigacaoAcessoriaComEmpresa(ObrigacaoAcessoriaInDBBase):
    """Schema para retorno de uma obrigação acessória com informações da empresa."""
    from .empresa import Empresa
    empresa: Empresa
