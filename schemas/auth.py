from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re

class UserRole(str, Enum):
    """Enum para os papéis de usuário no sistema."""
    ADMIN = "admin"
    USER = "user"
    AUDITOR = "auditor"

class UserBase(BaseModel):
    """Schema base para usuários."""
    email: EmailStr = Field(..., description="Endereço de e-mail do usuário")
    nome: str = Field(..., min_length=3, max_length=100, description="Nome completo do usuário")
    role: UserRole = Field(default=UserRole.USER, description="Papel do usuário no sistema")

class UserCreate(UserBase):
    """Schema para criação de um novo usuário."""
    senha: str = Field(
        ..., 
        min_length=8, 
        max_length=100,
        description="Senha do usuário (mínimo 8 caracteres, contendo letras e números)"
    )
    
    @validator('senha')
    def validar_senha(cls, v):
        """Valida a força da senha."""
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not re.search("[a-zA-Z]", v):
            raise ValueError("A senha deve conter pelo menos uma letra")
        if not re.search("\d", v):
            raise ValueError("A senha deve conter pelo menos um número")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "nome": "Fulano de Tal",
                "senha": "senhaSegura123",
                "role": "user"
            }
        }

class UserUpdate(BaseModel):
    """Schema para atualização de um usuário existente."""
    email: Optional[EmailStr] = Field(None, description="Novo endereço de e-mail do usuário")
    nome: Optional[str] = Field(None, min_length=3, max_length=100, description="Novo nome do usuário")
    senha: Optional[str] = Field(None, min_length=8, max_length=100, description="Nova senha do usuário")
    ativo: Optional[bool] = Field(None, description="Status de ativação do usuário")
    role: Optional[UserRole] = Field(None, description="Novo papel do usuário no sistema")

    class Config:
        schema_extra = {
            "example": {
                "nome": "Novo Nome do Usuário",
                "email": "novoemail@exemplo.com",
                "senha": "novaSenha123",
                "ativo": True,
                "role": "user"
            }
        }

class UserInDBBase(UserBase):
    """Schema base para usuários armazenados no banco de dados."""
    id: int
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True

class User(UserInDBBase):
    """Schema para retorno de dados do usuário."""
    pass

class UserInDB(UserInDBBase):
    """Schema para usuário no banco de dados (inclui senha hash)."""
    senha_hash: str

class Token(BaseModel):
    """Schema para o token de acesso JWT."""
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    """Schema para os dados armazenados no token JWT."""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

class Login(BaseModel):
    """Schema para dados de login."""
    email: EmailStr
    senha: str = Field(..., min_length=1, description="Senha do usuário")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "senha": "senhaSegura123"
            }
        }
