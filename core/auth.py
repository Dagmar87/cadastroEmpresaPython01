from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..config.settings import settings

# Configuração do contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do esquema OAuth2 para autenticação via token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Funções auxiliares
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    
    Args:
        plain_password: Senha em texto puro
        hashed_password: Hash da senha armazenado no banco de dados
        
    Returns:
        bool: True se a senha estiver correta, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera um hash para a senha fornecida.
    
    Args:
        password: Senha em texto puro
        
    Returns:
        str: Hash da senha
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token de acesso JWT.
    
    Args:
        data: Dados a serem incluídos no token
        expires_delta: Tempo de expiração do token
        
    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def get_user(db: Session, email: str) -> Optional[models.Usuario]:
    """
    Obtém um usuário pelo e-mail.
    
    Args:
        db: Sessão do banco de dados
        email: E-mail do usuário
        
    Returns:
        Optional[models.Usuario]: O usuário encontrado ou None
    """
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.Usuario]:
    """
    Autentica um usuário com e-mail e senha.
    
    Args:
        db: Sessão do banco de dados
        email: E-mail do usuário
        password: Senha em texto puro
        
    Returns:
        Optional[models.Usuario]: O usuário autenticado ou None
    """
    user = get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.senha_hash):
        return None
    return user

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> models.Usuario:
    """
    Obtém o usuário atual a partir do token JWT.
    
    Args:
        db: Sessão do banco de dados
        token: Token JWT
        
    Returns:
        models.Usuario: O usuário autenticado
        
    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: models.Usuario = Depends(get_current_user),
) -> models.Usuario:
    """
    Verifica se o usuário atual está ativo.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        models.Usuario: O usuário ativo
        
    Raises:
        HTTPException: Se o usuário estiver inativo
    """
    if not current_user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

async def get_current_active_superuser(
    current_user: models.Usuario = Depends(get_current_user),
) -> models.Usuario:
    """
    Verifica se o usuário atual é um superusuário.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        models.Usuario: O superusuário
        
    Raises:
        HTTPException: Se o usuário não for um superusuário
    """
    if not current_user.role == schemas.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem privilégios suficientes"
        )
    return current_user
