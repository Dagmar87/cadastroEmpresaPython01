from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Empresa, ObrigacaoAcessoria
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class EmpresaRequest(BaseModel):
    nome: str = Field(min_length=1, max_length=255)
    cnpj: str = Field(max_length=18)
    endereco: str = Field(min_length=1, max_length=600)
    email: str = Field(min_length=1, max_length=255)
    telefone: str = Field(max_length=11)

class ObrigacaoAcessoriaRequest(BaseModel):
    nome: str = Field(min_length=1, max_length=255)
    periodicidade: str(min_length=1, max_length=255)
