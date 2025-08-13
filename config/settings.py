from pydantic import BaseSettings, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    # Configurações do banco de dados
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/empresas_db"
    
    # Configurações de autenticação
    SECRET_KEY: str = "sua_chave_secreta_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    
    # Configurações da aplicação
    DEBUG: bool = True
    PROJECT_NAME: str = "Cadastro de Empresas API"
    VERSION: str = "1.0.0"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
