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
    periodicidade: str = Field(min_length=1, max_length=255)
    empresa_id: int

# Listar todas as empresas
@app.get('/empresas', status_code=status.HTTP_200_OK)
async def read_all_empresas(db: db_dependency):
    return db.query(Empresa).all()

# Procurar uma empresa especifica pelo id
@app.get('/empresa/{empresa_id}', status_code=status.HTTP_200_OK)
async def get_empresa_by_id(db: db_dependency, empresa_id: int = Path(gt=0)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if empresa is not None:
        return empresa
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Empresa não encontrada')

# Criar uma nova empresa
@app.post('/empresa', status_code=status.HTTP_201_CREATED)
async def create_empresa(db: db_dependency, empresa_request: EmpresaRequest):
    new_empresa = Empresa(**empresa_request.model_dump())

    db.add(new_empresa)
    db.commit()

# Editar uma empresa existente
@app.put('/empresa/{empresa_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_empresa(db: db_dependency, empresa_request: EmpresaRequest, empresa_id: int = Path(gt=0)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Empresa não encontrada')    
    
    for var, value in vars(empresa_request).items():
        setattr(empresa, var, value) if value else None

    db.commit()

# Excluir uma empresa
@app.delete('/empresa/{empresa_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_empresa(db: db_dependency, empresa_id: int = Path(gt=0)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Empresa não encontrada')
    
    db.delete(empresa)
    db.commit()