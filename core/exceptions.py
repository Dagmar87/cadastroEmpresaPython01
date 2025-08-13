from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from typing import Any, Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Classe base para exceções da aplicação."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.error_code = error_code or f"ERR_{status_code}"
        super().__init__(message)

class NotFoundError(AppError):
    """Exceção para recursos não encontrados."""
    
    def __init__(self, resource: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"{resource} não encontrado(a)",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details or {},
            error_code="NOT_FOUND"
        )

class ValidationError(AppError):
    """Exceção para erros de validação."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details or {},
            error_code="VALIDATION_ERROR"
        )

class UnauthorizedError(AppError):
    """Exceção para erros de autenticação/autorização."""
    
    def __init__(self, message: str = "Não autorizado"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED"
        )

class ForbiddenError(AppError):
    """Exceção para acesso negado."""
    
    def __init__(self, message: str = "Acesso negado"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN"
        )

class ConflictError(AppError):
    """Exceção para conflitos (ex: registro duplicado)."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details or {},
            error_code="CONFLICT"
        )

def setup_exception_handlers(app):
    """Configura os manipuladores de exceção da aplicação."""
    
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        """Manipula exceções personalizadas da aplicação."""
        logger.error(
            f"AppError: {exc.message}",
            extra={
                "status_code": exc.status_code,
                "details": exc.details,
                "error_code": exc.error_code,
                "path": request.url.path,
                "method": request.method,
            },
            exc_info=True
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )
    
    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        """Manipula exceções HTTP do FastAPI."""
        logger.warning(
            f"HTTPException: {exc.detail}",
            extra={
                "status_code": exc.status_code,
                "path": request.url.path,
                "method": request.method,
            },
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": exc.detail,
                    "details": getattr(exc, "details", {}),
                }
            },
            headers=getattr(exc, "headers", None),
        )
    
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        """Manipula erros de validação do FastAPI."""
        logger.warning(
            "Erro de validação na requisição",
            extra={
                "errors": json.loads(exc.json()),
                "path": request.url.path,
                "method": request.method,
            },
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Erro de validação nos dados fornecidos",
                    "details": {"errors": json.loads(exc.json())},
                }
            },
        )
    
    @app.exception_handler(ValidationError)
    async def handle_pydantic_validation_error(request: Request, exc: ValidationError):
        """Manipula erros de validação do Pydantic."""
        logger.warning(
            "Erro de validação no modelo",
            extra={
                "errors": exc.errors(),
                "path": request.url.path,
                "method": request.method,
            },
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Erro de validação nos dados fornecidos",
                    "details": {"errors": exc.errors()},
                }
            },
        )
    
    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        """Manipula exceções genéricas não tratadas."""
        logger.critical(
            "Erro interno do servidor",
            exc_info=exc,
            extra={
                "path": request.url.path,
                "method": request.method,
            },
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Ocorreu um erro inesperado no servidor",
                    "details": {"error": str(exc)} if app.debug else {},
                }
            },
        )
