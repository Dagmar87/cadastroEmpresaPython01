from typing import Generic, TypeVar, List, Optional
from pydantic.generics import GenericModel
from pydantic import Field

T = TypeVar('T')

class PaginatedResponse(GenericModel, Generic[T]):
    """
    Modelo genérico para respostas paginadas.
    
    Attributes:
        items: Lista de itens da página atual
        total: Número total de itens
        page: Número da página atual
        size: Número de itens por página
        pages: Número total de páginas
    """
    items: List[T]
    total: int = Field(..., ge=0, description="Número total de itens")
    page: int = Field(..., ge=1, description="Número da página atual")
    size: int = Field(..., ge=1, le=100, description="Número de itens por página")
    pages: int = Field(..., ge=0, description="Número total de páginas")

class PaginationParams:
    """
    Parâmetros de paginação para consultas ao banco de dados.
    
    Attributes:
        page: Número da página (começando em 1)
        size: Número de itens por página (máximo 100)
    """
    def __init__(
        self,
        page: int = 1,
        size: int = 10
    ):
        self.page = max(1, page)
        self.size = max(1, min(size, 100))  # Limita o tamanho da página a 100 itens

    @property
    def offset(self) -> int:
        """Calcula o deslocamento para a consulta SQL."""
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        """Retorna o limite de itens por página."""
        return self.size

def paginate(query, pagination: PaginationParams, schema):
    """
    Aplica paginação a uma consulta SQLAlchemy e retorna os resultados paginados.
    
    Args:
        query: Consulta SQLAlchemy
        pagination: Parâmetros de paginação
        schema: Schema Pydantic para serialização dos itens
        
    Returns:
        PaginatedResponse: Resposta paginada contendo os itens e metadados de paginação
    """
    total = query.count()
    items = query.offset(pagination.offset).limit(pagination.limit).all()
    
    return PaginatedResponse(
        items=[schema.from_orm(item) for item in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=(total + pagination.size - 1) // pagination.size if pagination.size > 0 else 0
    )
