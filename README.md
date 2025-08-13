# Sistema de Gerenciamento de Empresas e Obrigações Acessórias

## Visão Geral

API desenvolvida com FastAPI para gerenciamento de empresas e suas obrigações acessórias junto ao governo. A aplicação oferece autenticação JWT, CRUD completo para empresas e obrigações acessórias, validação de dados, paginação e tratamento de erros padronizado.

## Tecnologias

- **Backend**: Python 3.9+
- **Framework**: FastAPI
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Validação de Dados**: Pydantic v2
- **Autenticação**: JWT (JSON Web Tokens)
- **Documentação**: Swagger UI e ReDoc
- **Testes**: pytest
- **Controle de Versão**: Git

## Pré-requisitos

- Python 3.9 ou superior
- PostgreSQL 12+
- pip (gerenciador de pacotes do Python)
- virtualenv (recomendado)

## Instalação

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/Dagmar87/cadastroEmpresaPython01.git
   cd cadastroEmpresaPython01
   ```

2. **Configurar ambiente virtual**
   ```bash
   # Criar ambiente virtual
   python -m venv venv
   
   # Ativar ambiente (Windows)
   venv\Scripts\activate
   
   # Ativar ambiente (Linux/MacOS)
   source venv/bin/activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variáveis de ambiente**
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` com suas configurações locais.

5. **Executar migrações**
   ```bash
   # Criar tabelas no banco de dados
   alembic upgrade head
   ```

6. **Iniciar o servidor**
   ```bash
   uvicorn app.main:app --reload
   ```

## Autenticação

A API utiliza autenticação JWT (JSON Web Tokens). Para autenticar, envie uma requisição POST para `/api/v1/auth/login` com email e senha.

### Endpoints de Autenticação

- `POST /api/v1/auth/login` - Realiza login e retorna token JWT
- `POST /api/v1/auth/registrar` - Cria um novo usuário
- `GET /api/v1/auth/eu` - Retorna informações do usuário autenticado
- `POST /api/v1/auth/test-token` - Testa se o token é válido

### Como usar o token

Após o login, inclua o token nas requisições através do header `Authorization`:
```
Authorization: Bearer seu_token_jwt_aqui
```

## Documentação da API

A documentação interativa da API está disponível nos seguintes formatos:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testes

Para executar os testes:

```bash
pytest
```

## Funcionalidades

- Autenticação JWT
- CRUD de Empresas
- CRUD de Obrigações Acessórias
- Validação de CNPJ
- Paginação em listagens
- Tratamento de erros padronizado
- Documentação interativa
- Testes automatizados

## Estrutura do Projeto

```
cadastroEmpresaPython01/
├── alembic/               # Migrações do banco de dados
├── app/
│   ├── api/               # Rotas da API
│   │   ├── v1/            # Versão 1 da API
│   │   │   ├── endpoints/  # Endpoints agrupados por domínio
│   │   │   └── api.py     # Configuração do router da API v1
│   ├── core/              # Código central da aplicação
│   │   ├── auth.py        # Lógica de autenticação
│   │   ├── config.py      # Configurações da aplicação
│   │   └── security.py    # Utilitários de segurança
│   ├── db/                # Configuração do banco de dados
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Schemas Pydantic
│   └── main.py            # Ponto de entrada da aplicação
├── tests/                 # Testes automatizados
├── .env.example           # Exemplo de variáveis de ambiente
├── .gitignore
├── alembic.ini            # Configuração do Alembic
├── requirements.txt        # Dependências do projeto
└── README.md              # Este arquivo
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

- **Nome**: José Dagmar Florentino da Silva Sobrinho
- **Email**: [seu-email@exemplo.com]
- **LinkedIn**: [seu-linkedin]
