from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Cria a conexão com o banco de dados
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica a conexão antes de usá-la
    pool_recycle=300,    # Recicla conexões após 5 minutos
)

# Sessão local para interação com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos
Base = declarative_base()

def get_db():
    """
    Fornece uma instância de sessão do banco de dados.
    
    Yields:
        Session: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()