# Projeto de Análise e Projeto de Sistemas: Gestão de Itens

Este repositório contém o código-fonte do backend para um sistema de gestão de produtos e itens, desenvolvido como parte da disciplina de Análise e Projeto de Sistemas.

A API é construída em Python usando o framework FastAPI e se conecta a um banco de dados PostgreSQL.

## Tecnologias e Ferramentas

* **Linguagem:** Python 3.10+
* **Framework Web (API):** FastAPI
* **Servidor ASGI:** Uvicorn
* **Banco de Dados:** PostgreSQL
* **ORM (Mapeamento Objeto-Relacional):** SQLAlchemy
* **Validação de Dados:** Pydantic
* **Editor de Código:** Visual Studio Code
* **Controle de Versão:** Git & GitHub

## Funcionalidades da API

A API atualmente suporta as seguintes funcionalidades:

* **Autenticação:** Sistema de login completo com tokens JWT.
* **Autorização:** Rotas protegidas e diferenciação de permissões entre usuários `administrador` e `usuario`.
* **Gerenciamento de Produtos:** CRUD completo para o catálogo de produtos (apenas admin).
* **Gerenciamento de Locais:** CRUD completo para os locais de estoque (apenas admin).
* **Gerenciamento de Itens:** CRUD para os itens do inventário, com permissões específicas por papel.
* **Lógica de Negócio:** Endpoint para transferência de itens entre locais com registro de histórico.
* **Dashboard:** Endpoint de agregação de dados para a visão do administrador.
* **Busca:** Filtragem de itens por local, status e número de série.

---



