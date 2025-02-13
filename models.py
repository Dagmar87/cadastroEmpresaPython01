from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)
    cnpj = Column(String, index=True, unique=True)
    endereco = Column(String, index=True)
    email = Column(String, index=True)
    telefone = Column(String, index=True)
    obrigacaoAcessorias = relationship("ObrigacaoAcessoria", back_populates="empresa")

class ObrigacaoAcessoria(Base):
    __tablename__ = 'obrigacaoAcessorias'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    periodicidade = Column(String, index=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)
    empresa = relationship("Empresa", back_populates="obrigacaoAcessorias")