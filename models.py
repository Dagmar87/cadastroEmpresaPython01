from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    empresas = relationship("Empresa", back_populates="responsavel")
    
    def __repr__(self):
        return f"<Usuario {self.email}>"

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False, index=True)
    cnpj = Column(String(14), unique=True, nullable=False, index=True)
    endereco = Column(String(600), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    telefone = Column(String(15), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Relacionamentos
    responsavel = relationship("Usuario", back_populates="empresas")
    obrigacoes_acessorias = relationship("ObrigacaoAcessoria", back_populates="empresa", 
                                       cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Empresa {self.nome} - {self.cnpj}>"

class PeriodicidadeEnum(str, enum.Enum):
    DIARIA = "Diária"
    SEMANAL = "Semanal"
    QUINZENAL = "Quinzenal"
    MENSAL = "Mensal"
    BIMESTRAL = "Bimestral"
    TRIMESTRAL = "Trimestral"
    SEMESTRAL = "Semestral"
    ANUAL = "Anual"
    EVENTUAL = "Eventual"

class ObrigacaoAcessoria(Base):
    __tablename__ = 'obrigacoes_acessorias'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    descricao = Column(String(1000), nullable=True)
    periodicidade = Column(Enum(PeriodicidadeEnum), nullable=False)
    data_vencimento = Column(DateTime(timezone=True), nullable=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id'), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    empresa = relationship("Empresa", back_populates="obrigacoes_acessorias")
    
    def __repr__(self):
        return f"<ObrigacaoAcessoria {self.nome} - {self.periodicidade}>"