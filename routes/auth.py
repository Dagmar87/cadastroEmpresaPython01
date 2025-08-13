from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas
from ..core import auth
from ..core.config import settings
from ..database import get_db

router = APIRouter(tags=["autenticacao"])

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Autentica um usuário e retorna um token de acesso.
    
    Parâmetros:
        form_data: Dados do formulário de login (username e password)
        db: Sessão do banco de dados
        
    Retorna:
        Token de acesso JWT
        
    Levanta:
        HTTPException: Se as credenciais estiverem incorretas ou o usuário estiver inativo
    """
    # Autentica o usuário
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Cria o token de acesso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/registrar", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Cria um novo usuário.
    
    Parâmetros:
        user_in: Dados do novo usuário
        db: Sessão do banco de dados
        
    Retorna:
        O usuário criado
        
    Levanta:
        HTTPException: Se o e-mail já estiver em uso
    """
    # Verifica se já existe um usuário com o mesmo e-mail
    db_user = auth.get_user(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já registrado"
        )
    
    # Cria o hash da senha
    hashed_password = auth.get_password_hash(user_in.senha)
    
    # Cria o usuário no banco de dados
    db_user = models.Usuario(
        email=user_in.email,
        nome=user_in.nome,
        senha_hash=hashed_password,
        role=user_in.role,
        ativo=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/eu", response_model=schemas.User)
async def read_users_me(
    current_user: models.Usuario = Depends(auth.get_current_active_user)
) -> Any:
    """
    Retorna os dados do usuário atualmente autenticado.
    
    Parâmetros:
        current_user: Usuário autenticado
        
    Retorna:
        Dados do usuário autenticado
    """
    return current_user

@router.post("/test-token", response_model=schemas.User)
async def test_token(
    current_user: models.Usuario = Depends(auth.get_current_active_user)
) -> Any:
    """
    Testa se o token de acesso é válido.
    
    Parâmetros:
        current_user: Usuário autenticado
        
    Retorna:
        Dados do usuário autenticado
    """
    return current_user
