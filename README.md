# cadastroEmpresaPython01

## Criação de uma API simples utilizando FastAPI, Pydantic, SQLAlchemy para cadastrar empresas e gerenciar obrigações acessórias que a empresa precisa declarar para o governo.

- Desafio Técnico: Desenvolvimento de uma API simples para cadastro de empresas e gerenciamento de obrigações acessórias que a empresa precisa declarar para o governo.
- Empresa: Dcifre
- Vaga: Estagiário(a) de Desenvolvimento de Software.
- Nome: José Dagmar Florentino da Silva Sobrinho

## Descrição

Esse projeto consiste na criação de uma API simples para cadastro de empresas e gerenciamento de obrigações acessórias que a empresa precisa declarar para o governo, utilizando a linguagem Python e suas bibliotecas e seus frameworks FastAPI, Pydantic e SQLAlchemy.

## Linguagens e Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Banco de Dados PostgreSQL
- Swagger UI
- IDE VSCode

## Instruções para rodar o projeto

Para rodar esse projeto, é necessario seguir as seguintes instruções abaixo:

1. git clone https://github.com/Dagmar87/cadastroEmpresaPython01.git
2. cd cadastroEmpresaPython01
3. cp .env.example .env (Fazer cópia .env.example para .env)
4. python -m pip install --user virtualenv
5. python -m virtualenv venv (Criar o ambiente de trabalho Python)
6. venv\Scripts\activate (Ativar o ambiente)
7. python -m pip install fastapi[all] sqlalchemy psycopg2 pydantic (Instalar as bibliotecas python do projeto)
8. uvicorn app:app (Rodar o projeto)
9. Acessar o seguinte endereço: http://127.0.0.1:8000 ou http://localhost:8000
10. Para visualizar e testar todas as APIs no Swagger UI, deve acessar o seguinte endereço: http://127.0.0.1:8000/docs ou http://localhost:8000/docs

## Operações CRUD do Projeto

Para visualizar as operações CRUD criadas no projeto e suas finalidades, deve acessar o seguinte link abaixo:

Link: https://github.com/Dagmar87/cadastroEmpresaPython01/blob/main/FastAPI%20-%20Swagger%20UI.pdf



